import os, datetime
from sys import stdout, stderr, exc_info
from traceback import print_exception
from multiprocessing import Pool, cpu_count
from ROOT import TFile, TTree, TChain, gROOT
from optparse import OptionParser
from contextlib import contextmanager, nested

from strSeqOption import strSeqOption
from redir import redir

def _makeChunk(chain, section, events):
    """Returns a generator that iterates over a subset of a TTree or TChain"""
    lastfile = None
    for iteration, entryNum in enumerate(xrange(section*events, (section+1)*events), start=1):
        if chain.GetEntry(entryNum):
            if chain.GetFile() != lastfile:
                if lastfile: print "Finished processing file", lastfile, "."
                print "Starting to process file", chain.GetFile().GetName(), "."
                lastfile = chain.GetFile()
            if iteration%1000 == 0:
                print "Section", section, "processing entry number", entryNum, \
                      ", event", iteration, "of", events, "in this section."
                stdout.flush()
            yield chain

def _outdir(location, selection, dataset, output, **ignored):
    """Return the name of the output directory for this job."""
    return os.path.join(location, selection, dataset[0], output[0], output[1])

def _waitforone(dir):
    """Block until dir/pending is deleted.  Then, if dir/crashed exists, raise an exception."""
    while os.access(os.path.join(dir, 'pending'), os.F_OK):
        sleep(120)
    if os.access(os.path.join(dir, 'crashed'), os.F_OK):
        raise RuntimeError('Input in %(dir)s has crashed section(s)'%{'dir': dir})

def _waitforinputs(location, selection, dataset, friend, **ignored):
    """Wait for all of our inputs to be ready."""
    stem = os.path.join(location, selection, dataset[0])
    for input in [os.path.join(stem, 'TopTree', dataset[1])] + [os.path.join(stem, f[0], f[1]) for f in friend]:
        _waitforone(input)

@contextmanager
def _inChain(selection, dataset, friend, location, section, events, **ignored):
    """Create the input TChain (chunked), with friend TChains."""
    stem = os.path.join(location, selection, dataset[0])
    # Make the primary chain
    chain = TChain('TopTree')
    chain.Add(os.path.join(stem, 'TopTree', dataset[1], "*.root"))
    # Make the friend chains and add them to the primary chain
    for f in friend:
        frchain = TChain(f[0])
        frchain.Add(os.path.join(stem, f[0], f[1], "*.root"))
        chain.AddFriend(frchain)
    yield _makeChunk(chain, section, events)

@contextmanager
def _outTree(output_files, output, section, **options):
    """Create output TTree in output TFile and close output TFile when we're done."""
    pendingdir = os.path.join(_outdir(output=output, **options), 'pending')
    outfilename = output[0]+"-"+str(section)+".root"
    output_files.append(outfilename)
    outfile = TFile(os.path.join(pendingdir, outfilename), "RECREATE")
    outtree = TTree(output[0], "")
    yield outtree
    outfile.Write()
    outfile.Close()

@contextmanager
def _logging(output_files, selection, dataset, friend, output, location, section, **ignored):
    """Create log and error files, and redirect all output to them."""
    pendingdir = os.path.join(_outdir(location, selection, dataset, output), 'pending')
    logname = output[0]+"-"+str(section)+".log"
    errname = output[0]+"-"+str(section)+".err"
    output_files.extend([logname, errname])
    with nested(redir(os.path.join(pendingdir, logname), stdout),
                redir(os.path.join(pendingdir, errname), stderr)):
        try:
            yield
        except:
            print_exception(*exc_info())
            raise

def _rmdir_if_empty(dir):
    """Remove a directory iff it is empty.  Return whether or not it was removed."""
    try:
        os.rmdir(dir)
        return True
    except OSError:
        return False

@contextmanager
def _place_output_files(selection, dataset, friend, output, location, section, events, **ignored):
    """Move output_files from a successful section from 'pending' into outdir,
    and output_files from a crashed section into 'crashed'.  Delete 'pending'
    if it is empty (because this was the last section)."""
    outdir = _outdir(location, selection, dataset, output)
    pendingdir = os.path.join(outdir, 'pending')
    output_files = []
    try:
        yield output_files
    except:
        crashdir = os.path.join(outdir, 'crashed')
        if not os.access(crashdir, os.F_OK): os.makedirs(crashdir)
        for file in output_files:
            os.rename(os.path.join(pendingdir, file), os.path.join(crashdir, file))
        _rmdir_if_empty(pendingdir)
        raise
    else:
        for file in output_files:
            os.rename(os.path.join(pendingdir, file), os.path.join(outdir, file))
        _rmdir_if_empty(pendingdir)

def _wrapAna(Ana, section, **options):
    """Calls your analysis function Ana after creating the input chain and output tree."""
    gROOT.SetBatch()
    _waitforinputs(**options)
    options['section'] = section
    with _place_output_files(**options) as output_files:
        with _logging(output_files, **options):
            with nested(_inChain(**options), _outTree(output_files, **options)) as (inChain, outTree):
                Ana(inChain, outTree, output_files=output_files, **options)

def _countEntries(location, selection, dataset, **ignored):
    """Return the number of entries in the TChain described by location, selection, and dataset."""
    chain = TChain('TopTree')
    chain.Add(os.path.join(location, selection, dataset[0], 'TopTree', dataset[1], '*.root'))
    print "Calculating number of entries in input.  This may take a little while if there are a lot of entries."
    totalEvents = chain.GetEntries()
    print "Dataset has", totalEvents, "entries."
    return totalEvents

def _make_output_dir(**options):
    """Create an output directory and 'latest' symlink to it, with a 'pending' directory inside."""
    outdir = _outdir(**options)
    pendingdir = os.path.join(outdir, 'pending')
    latestlink = os.path.normpath(os.path.join(outdir, "..", "latest"))
    print "Creating output directory:", outdir
    os.makedirs(outdir)
    print "Creating 'pending' directory:", pendingdir
    os.makedirs(pendingdir)
    print "Creating 'latest' symlink:", latestlink, '->', outdir
    if os.access(latestlink, os.F_OK): os.remove(latestlink)
    os.symlink(outdir, latestlink)

def poolSubmit(Ana, dataset, output, friend, events, pool=None, **other_options):
    """Submit appropriate number of sections to the given pool, or
    run a single section in this process."""
    # First, fix up the options we were given.
    if len(output) == 1: output.append(datetime.datetime.now().isoformat())
    if len(dataset) == 1: dataset.append('latest')
    for f in friend:
        if len(f) == 1: f.append('latest')
    friend = dict(friend)
    other_options.update({'dataset': dataset, 'output': output,
                          'friend': friend, 'events': events})

    _make_output_dir(**other_options)
    if pool:
        totalSections = int(_countEntries(**other_options) / events) + 1
        print "We will run", totalSections, "section(s) of", events, "each."
        for section in xrange(0, totalSections):
            pool.apply_async(_wrapAna, (Ana, section), other_options)
    else:
        _wrapAna(Ana, section=0, **other_options)

@contextmanager
def makePool(processes=-1, **ignored):
    """Create a process pool, and when the context is exited, close and join it."""
    print "Starting up a worker pool of", (processes-1) % cpu_count() + 1, "processes."
    pool = Pool((processes-1) % cpu_count() + 1)
    yield pool
    pool.close()
    pool.join()

def makeOptions():
    """Create an OptionParser object with our standard options."""
    parser = OptionParser(option_class=strSeqOption)
    parser.add_option('-s', '--selection', metavar="SELECTION")
    parser.add_option('-d', '--dataset', type='string-seq', action="append", metavar="DATASET[,TAG]", help="Primary tree to use.  Found in LOCATION/SELECTION/DATASET/TopTree/TAG/.  TAG defaults to 'latest'.")
    parser.add_option('-f', '--friend', type='string-seq', action="append", metavar="FRIEND[,TAG]", help="May be used more than once.  Friend tree(s) to use.  Found in LOCATION/SELECTION/DATASET/FRIEND/TAG/.  TAG defaults to 'latest'.")
    parser.add_option('-o', '--output', type='string-seq', metavar="OUTPUT[,TAG]", help="Name of output tree.  Will be put in LOCATION/SELECTION/DATASET/OUTPUT/TAG.  TAG defaults to the current date+time.  A symlink will be created named 'pending' while the job runs, and another symlink 'latest' after it is finished.")
    parser.add_option('-l', '--location', metavar="LOCATION", help="The parent directory of all trees: input, friends, and output.")
    parser.add_option('-e', '--events', type="int", default=5000, metavar="N", help="The number of events to process in each section.")
    parser.add_option('-p', '--processes', type="int", default=-1, metavar="N", help="Process pool size.  If N>1, pool size is N.  If N<=0, pool size is cpu_count() + N.")
    parser.add_option('-1', '--single', action="store_true", help="For debugging: Run only a single section in this process instead of submitting multiple sections to a process pool.")
    return parser

def runAna(Ana, parser=makeOptions(), **defaults):
    """Parse the command line arguments, create a process pool, then call poolSubmit."""
    # Apply the defaults and parse the command line options
    parser.set_defaults(**defaults)
    options = vars(parser.parse_args()[0])
    datasets = options.pop('dataset')
    parser.destroy()

    # Submit the sections to the process pool, with all that that entails
    if options.get('single', False):
        # For debugging.  Run a single section on a single dataset in this process.
        print "We will run a single section of", options.get('events'), "events."
        poolSubmit(Ana, dataset=datasets[0], **options)
    else:
        with makePool(**options) as pool:
            for dataset in datasets:
                poolSubmit(Ana, pool=pool, dataset=dataset, **options)
        pass


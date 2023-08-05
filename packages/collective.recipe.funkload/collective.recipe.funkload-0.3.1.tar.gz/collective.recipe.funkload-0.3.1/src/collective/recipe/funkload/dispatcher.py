import os
import sys
import collective.funkload.bench
import collective.funkload.recorder
import funkload.ReportBuilder
import funkload.Recorder
import datetime

class FunkloadWrapper(object):
    
    def __init__(self,url,buildout_dir,data_dir,report_dir,record_dir,record_name,record_port):
        self._url = url
        self._dir = buildout_dir
        self._report_dir = report_dir
        self._data_dir = data_dir
        self._record_dir = record_dir
        self._record_name = record_name
        self._record_port = record_port
    
    def _usage(self):
        """ Print usage """
        print "Usage:"
        for method in self._getActions():
            method = getattr(self,method)
            print str(method.__name__) + ": " + str(method.__doc__)
    
    def _getActions(self):
        return [x for x in dir(self) if not x.startswith('_')]
    
    def _dispatch(self):
        self._args = sys.argv
        actions = self._getActions()
        try:
            action = self._args[1]
        except IndexError:
            action = None

        self._clean_args = [self._args[0]] + self._args[2:]

        if action and action in actions:
            if len(self._args[2:]): #if argument don t filter path
                test_path = ['--test-path=%s' % (path) for path in sys.path]
            else:
                test_path = ['--test-path=%s' % (path) for path in sys.path if path.startswith(self._dir) and path != self._dir]
            
            self._injected_args = [self._args[0]] + test_path + ['--url=%s' % self._url] +  self._args[2:]
            action = getattr(self,action)
            action()
        else:
            self._usage()
          
        
    def test(self):
        """ Launch a FunkLoad unit test. """
        raise NotImplementedError

    def bench(self):
        """ Launch a FunkLoad unit test as load test. """
        dir_name = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        target = os.path.join(self._data_dir,dir_name)
        os.makedirs(target)
        os.chdir(target)
        collective.funkload.bench.run(args=self._injected_args)
        self.report(no_args=True)
        

    def _getRecentReportContent(self):
        result_sets = os.listdir(self._data_dir)
        result_sets.sort()
        most_recent = result_sets[-1]
        if most_recent:
            recent_path = os.path.join(self._data_dir,most_recent)
        else:
            return []
        
        files = os.listdir(recent_path)
        result = []
        for f in files:
            filename = os.path.join(recent_path,f)
            if f.endswith('.xml') and os.path.getsize(filename):
                result.append(filename)
        return result


    def report(self,no_args=False):
        """ Generate a report from the most recent bench result """
        dir_name = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        target = os.path.join(self._report_dir,dir_name)
        os.makedirs(target)
        os.chdir(target)

        if no_args:
            self._clean_args = self._clean_args[:1]
        if len(self._clean_args) > 1 and not no_args:
            print "Found extra command line arguments, passing command through unadjusted"
            sys.argv = self._clean_args[:]
            funkload.ReportBuilder.main()
            return
            
        xml_list = self._getRecentReportContent()
        for f in xml_list:
            sys.argv = self._clean_args[:]
            extra_args = ['--html','-o',target,f]
            sys.argv += extra_args
            try:
                funkload.ReportBuilder.main()
            except:
                print "Report generation failed for %s" % (f)


    def record(self):
        """Launch a TCPWatch proxy and record activities, then output a 
        FunkLoad script or generates a FunkLoad unit test if test_name is specified."""
        dir_name = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        base_dir = os.path.join(self._record_dir,self._record_name)
        target = os.path.join(base_dir, dir_name)
        os.makedirs(target)
        os.chdir(target)
        
        #Building parameters:
        user_argv = self._args[2:]
        recipe_argv = [self._record_name, '-p %s' % self._record_port]
        argv = user_argv or recipe_argv
        
        recorder = collective.funkload.recorder.RecorderProgram(argv=argv)
        recorder.run()

            
def main(url,buildout_dir,report_destination,data_destination,record_output,record_test_name,record_proxy_port):
    wrapper = FunkloadWrapper(url,buildout_dir,data_destination,report_destination,record_output,record_test_name,record_proxy_port)
    wrapper._dispatch()

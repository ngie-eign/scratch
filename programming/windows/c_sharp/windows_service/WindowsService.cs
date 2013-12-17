using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.ServiceProcess;
using System.Text;
using System.Threading;

namespace WindowsService
{

    public class WindowsService : System.ServiceProcess.ServiceBase
    {

        public Process proc;

        public WindowsService()
        {
            string exe = Process.GetCurrentProcess().MainModule.FileName;

            this.AutoLog = true;
            this.ServiceName = "WindowsService";
            this.CanPauseAndContinue = false;
            this.CanStop = true;

            this.proc = new Process();
            this.proc.EnableRaisingEvents = true;
            this.proc.StartInfo.RedirectStandardOutput = false;
            this.proc.StartInfo.RedirectStandardError = false;
            this.proc.StartInfo.UseShellExecute = !(
                this.proc.StartInfo.RedirectStandardOutput ||
                this.proc.StartInfo.RedirectStandardError
            );

            this.proc.StartInfo.FileName =
                System.IO.Path.GetDirectoryName(exe) + @"\run_service.cmd";
        }

        private void ProcessListen()
        {
            this.proc.WaitForExit();
            this.ExitCode = this.proc.ExitCode;
            this.Stop();
        }

        protected override void OnStart(string[] args)
        {
            this.proc.Start();
            Thread thread = new Thread(ProcessListen);
            thread.Start();
            // XXX: thread is never joined; shouldn't be an issue as long as
            // the app exits properly.
        }

        protected override void OnStop()
        {
            if (!this.proc.HasExited)
            {
                this.proc.Kill();
            }
        }

        public static void Main()
        {
            System.ServiceProcess.ServiceBase.Run(new WindowsService());
        }

    }

}

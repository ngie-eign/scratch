--- libexec/telnetd/sys_term.c	1999-05-18 00:26:58.000000000 -0700
+++ libexec/telnetd/sys_term.c	2012-11-16 20:29:52.249668332 -0800
@@ -1694,8 +1694,8 @@
 #endif
 	utmpx.ut_type = LOGIN_PROCESS;
 	(void) time(&utmpx.ut_tv.tv_sec);
-	if (makeutx(&utmpx) == NULL)
-		fatal(net, "makeutx failed");
+	if (pututxline(&utmpx) == NULL)
+		fatal(net, "pututxline failed");
 #endif
 	scrub_env();
 	
@@ -2228,8 +2228,10 @@
 	utxp = getutxline(&utmpx);
 	if (utxp) {
 		utxp->ut_type = DEAD_PROCESS;
+#ifdef HAVE_STRUCT_UTMPX_UT_EXIT
 		utxp->ut_exit.e_termination = 0;
 		utxp->ut_exit.e_exit = 0;
+#endif
 		(void) time(&utmpx.ut_tv.tv_sec);
 		utmpx.ut_tv.tv_usec = 0;
 #ifdef MAGIC_UTMPX_NAME

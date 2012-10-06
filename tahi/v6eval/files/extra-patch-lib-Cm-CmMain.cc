--- lib/Cm/CmMain.cc
+++ lib/Cm/CmMain.cc
@@ -47,7 +47,7 @@
 #include <string.h>
 #include <stdlib.h>
 #include <unistd.h>
-#include <utmp.h>
+#include <utmpx.h>
 #include <time.h>
 #include <pwd.h>
 #include <sys/time.h>
@@ -128,19 +128,28 @@
 
 //----------------------------------------------------------------------
 // æ„≥≤≤Ú¿œæ Û∫Ó¿Æ
-static struct utmp *myUtmpEnt(FILE *in,struct utmp *u) {
-	int s=ttyslot();
-	if(s<0||fseek(in,sizeof(struct utmp)*s,0)<0||
-		fread(u,sizeof(struct utmp),1,in)==0) {return 0;}
-	return u;}
 void CmMain::makeCatch2Eye(STR p) {
 static char catch2[]=" on %*.*s:%-*.*s from %*.*s";
-	struct utmp ux[1], *u; FILE *in;
-	if((in=fopen("/etc/utmp","r"))==NULL) {return;}
-	u=myUtmpEnt(in,ux); fclose(in);
-	if(!u) {return;}
+	struct utmpx ul, *u;
+	const char *tty;
+
+	tty = ttyname(0);
+	if (tty == NULL)
+		tty = ttyname(1);
+	if (tty == NULL)
+		tty = ttyname(2);
+	if (tty == NULL)
+		return;
+	if (strncmp(tty, "/dev/", 5) == 0)
+		tty += 5;
+	strncpy(ul.ut_line, tty, sizeof(ul.ut_line));
+	setutxent();
+	u = getutxline(&ul);
+	endutxent();
+	if (u == NULL || u->ut_type != USER_PROCESS)
+		return;
 #define A(a)sizeof(a),sizeof(a),a
-	sprintf(p,catch2,A(u->ut_line),A(u->ut_name),A(u->ut_host));
+	sprintf(p,catch2,A(u->ut_line),A(u->ut_user),A(u->ut_host));
 #undef A
 	return;}
 void CmMain::makeCatchEye(const STR pgmName) {

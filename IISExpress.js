/*
Esse script é utilizado para iniciar o IIS Express, um servidor web de desenvolvimento para o Windows, 
sem uma janela de console (quando iniciado com o wscript.exe). Ele define algumas variáveis de configuração, 
como a porta em que o servidor deve ser iniciado e o caminho do site que será servido. Em seguida, ele cria os
objetos "Scripting.FileSystemObject" e "WScript.Shell" para ter acesso a funcionalidades do sistema de arquivos
e do shell do Windows, respectivamente. Em seguida, ele procura o arquivo de instalação do IIS Express no sistema 
e, se encontrado, inicia o servidor com as configurações especificadas. O servidor será iniciado escondido e o script 
aguardará até que ele seja encerrado.
*/
// Runs IIS Express without a console window (if started with wscript.exe)

var sitePort = 8080;
var sitePath = ".";
var siteClr = "v4.0";

var fso = new ActiveXObject("Scripting.FileSystemObject");
var wshell = new ActiveXObject("WScript.Shell");

// Resolve path
sitePath = fso.GetAbsolutePathName(sitePath) + "\\www";

// look for IISExpress
var iisexpress = wshell.ExpandEnvironmentStrings("%ProgramFiles%\\IIS Express\\iisexpress.exe");
if (!fso.FileExists(iisexpress)) {
    iisexpress = wshell.ExpandEnvironmentStrings("%ProgramFiles(x86)%\\IIS Express\\iisexpress.exe");

    if (!fso.FileExists(iisexpress)) {
        WScript.Echo("Couldn't find IIS Express. Install using the Web Platform Installer.");
        WScript.Quit(1);
    }    
}

// launch browser
//wshell.Run('http://localhost:' + sitePort, 1, false);

// start IISExpress hidden and wait for exit
wshell.Run('"' + iisexpress + '" /port:' + sitePort + ' /path:"' + sitePath + '"', 0, true);
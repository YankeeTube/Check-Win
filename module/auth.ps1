Set-ExecutionPolicy RemoteSigned
$share=get-wmiobject win32_share
foreach ($wmi in $share) {net share $wmi.name}
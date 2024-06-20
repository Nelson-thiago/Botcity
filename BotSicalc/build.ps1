$exclude = @("venv", "BotSicalc.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "BotSicalc.zip" -Force
$exclude = @("venv", "BotSicalc2.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "BotSicalc2.zip" -Force
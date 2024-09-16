$exclude = @("venv", "BotCotacao2.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "BotCotacao2.zip" -Force
Write-Host "Downloading MySQL Installer..." -ForegroundColor Green
Invoke-WebRequest -Uri 'https://dev.mysql.com/get/Downloads/MySQLInstaller/mysql-installer-community-5.7.41.0.msi' -OutFile 'mysql-installer-community-5.7.41.0.msi'

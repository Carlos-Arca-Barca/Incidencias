@echo off

echo Iniciando backup...

for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set dt=%%I

set YYYY=%dt:~0,4%
set MM=%dt:~4,2%
set DD=%dt:~6,2%
set HH=%dt:~8,2%
set Min=%dt:~10,2%

set FILENAME=backup_%YYYY%_%MM%_%DD%_%HH%_%Min%.sql

"C:\Program Files\PostgreSQL\18\bin\pg_dump.exe" "postgresql://neondb_owner:npg_b2tJuwFrOT3m@ep-lucky-grass-abud7vle-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require" > "D:\Incidencias\%FILENAME%"

echo Backup creado en D:\Incidencias\%FILENAME%

pause
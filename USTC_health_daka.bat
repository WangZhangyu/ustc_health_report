@echo off
@title �ƴ�ÿ�ս��������ýű�
@echo.========================================================================
@echo ע�⣺�Ҽ�����ѡ���Թ���Ա������С�������ᵼ�³�������ʧ�ܡ�
@echo.========================================================================
@echo.
cd /d %~dp0
set /p choice="ȷ�ϰ�װ�밴[y]�س���ж�س����밴[d]�س���ȡ�������밴[n]�س� "
if %choice%==n goto na
if %choice%==y goto ya
if %choice%==d goto del

pause
exit

:ya
@echo.
set "output=auto_submit.bat"
echo @echo off > %output%
echo echo Hello  welcome! start ... >> %output%
echo %cd:~0,2% >> %output%
echo cd %cd% >> %output%
echo python main.py >> %output%
echo pause >> %output%
echo %output% �Ѵ���...


@echo.
REM Ĭ�϶�ʱִ��ʱ��Ϊ08:10�����Ը���set_time����ʽΪ HH��MM��
set set_time=08:10
SCHTASKS /CREATE /TN Auto_USTC_health_task /sc DAILY /st %set_time% /tr %cd%\auto_submit.bat
@echo.
schtasks /query /tn Auto_USTC_health_task
@echo.
pause


:na
@echo.
@echo ��������˳�����
@echo.
@pause >nul
exit



:del
@echo.
SCHTASKS /DELETE /TN Auto_USTC_health_task 
@echo.
pause


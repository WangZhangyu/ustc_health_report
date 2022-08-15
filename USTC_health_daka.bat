@echo off
@title 科大每日健康打卡配置脚本
@echo.========================================================================
@echo 注意：右键程序，选择“以管理员身份运行”，否则会导致程序运行失败。
@echo.========================================================================
@echo.
cd /d %~dp0
set /p choice="确认安装请按[y]回车，卸载程序请按[d]回车，取消操作请按[n]回车 "
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
echo %output% 已创建...


@echo.
REM 默认定时执行时间为08:10，可以更改set_time（格式为 HH：MM）
set set_time=08:10
SCHTASKS /CREATE /TN Auto_USTC_health_task /sc DAILY /st %set_time% /tr %cd%\auto_submit.bat
@echo.
schtasks /query /tn Auto_USTC_health_task
@echo.
pause


:na
@echo.
@echo 按任意键退出程序！
@echo.
@pause >nul
exit



:del
@echo.
SCHTASKS /DELETE /TN Auto_USTC_health_task 
@echo.
pause


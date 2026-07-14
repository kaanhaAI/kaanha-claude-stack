@echo off
rem dev hub (Windows): run any command with the Node.js toolchain on PATH.
rem Copy to withnode.cmd and set YOUR Node.js install directory below.
rem Usage: withnode.cmd <command> [args...]
set "PATH=C:\path\to\your\nodejs;%PATH%"
%*

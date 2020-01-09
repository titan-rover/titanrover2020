#!/usr/bin/env bash
NODEPATH="$HOME/$HOSTNAME/Programs/UI_Data"
GREP=$(ps a | grep "Launch.js" | grep -v "grep")
#PID=$(ps -e | grep $CAT)
#setPID () {
#    cd /
#    cd tmp
#    echo $$ > rosuiserver
#}
set -x #comment this to see process steps output to terminal
CHECK=$(systemctl is-active roverui.service)
if [[ "$CHECK" != "active" ]] && [[ "$GREP" == "" ]]
then
    WINDOW=$(zenity --question --text "RoverUI daemon inactive, start service?" --no-wrap --ok-label "Yes" --cancel-label "No"; echo $?)
    if [ $WINDOW == 0 ]
    then
        printf "\n"; echo "$(tput setaf 3)Starting server...$(tput srgr0)"; source $HOME/.nvm/nvm.sh; cd /; cd home/$HOSTNAME/Programs/UI_Data ;nvm use node; node Launch.js & xdg-open http://localhost:9000 ; exit;
    elif [ $WINDOW == 1 ]
    then
        printf "\n"; echo "exiting...";exit;
    fi
else
    printf "\n"; echo "JS server running";xdg-open http://localhost:9000; exit;
fi

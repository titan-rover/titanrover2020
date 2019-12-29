#!/bin/bash

#NOTE: MAKE SURE TO CHANGE 'GORDON' TO YOUR PROPER HOST NAME
#NOTE: MAKE SURE TO CHANGE PATHWAY ON LINE 10 AND 26 TO /home/YOUR_HOSTNAME/catkin_ws/src
#NOTE: GIT LINK IN LINE 10 IS FOR THE BASESTATION REPO, CHANGE LINK ACCORDINGLY TO YOUR DESIRED REPO  

cd /home/gordon
mkdir gittemp #make a folder, clone the given repo into it
cd gittemp
git clone https://github.com/titan-rover/base_station.git
SRC="/home/gordon/test1/src" #change gordon to $HOSTNAME
GIT="/home/gordon/gittemp/base_station/src"
DIFF=$(diff -r $GIT $SRC) #compare contents of local src folder to git clone using DIFF

echo "Finding difference between GIT repo and local SRC ..."
echo $DIFF 
if [ "$DIFF" != "" ] 
then
    echo "---Changes in directory contents found.---"; echo #;
else
    echo "---No changes in directories found.---";
fi

while true; do
	read -p "Replace contents of local SRC with the contents of GIT folder (Y\N)?: " yn
	case $yn in
		[Yy]* ) rm -R /home/gordon/test1/src;mv -T $GIT $SRC; rm -R /home/gordon/gittemp/;break;; #remove old local src, move cloned src into local folder, remove temp git folder
		[Nn]* ) echo "exiting.";rm -R /home/gordon/gittemp;exit;; #if no then remove the temp GIT clone folder
		*) echo "Please answer Y or N.";;
	esac
done


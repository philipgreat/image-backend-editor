function commit() { 
	local message="$1" 
	local msgprefix="$2"
	local finalmessage="${msgprefix}${message}"
	local codePath="./" 
	git add "$codePath" 
	git commit -m "${finalmessage}" 
	git pull
	git push
	echo ""
	echo "committed @ $(date '+%Y-%m-%d %H:%M:%S')" 
	echo "" 
}


function officeserver(){
	ssh -p 6543 philip@t420.doublechaintech.cn $1
}

commit "make change"

officeserver "cd ~/githome/image-backend-editor/ && git pull"
officeserver "cd ~/githome/image-backend-editor/ && python3 reactize-image.py"

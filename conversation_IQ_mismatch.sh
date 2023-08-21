check(){
    echo $1
    if [ -f $1 ]; then 
        rm $1
        curState=true
    else
        curState=false
    fi
}
ERR_PATH="/data/lessIsMore/instanceScore/openai-proxy/Clear_LLaVa/output_err/err_conversation_IQ_mismatch.txt"
flag=false

while true
do
    if [ $flag == false ]; then
        flag=true
        python3 conversation_IQ_mismatch.py
    fi
    check $ERR_PATH
    if [ $curState == true ]; then  
        flag=false
    fi
done

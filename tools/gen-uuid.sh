uuid() {
    ret="$(uuidgen)"
    ret="${ret//-/}"
    ret=$(echo "$ret" |  tr '[:upper:]' '[:lower:]' )
    echo $ret
    return
}
## 환경변수 다운받고 다시 업로드 하는 구문

$ printenv > environment_backup.txt

$ while read line; do export "$line"; done < environment_backup.txt

## .sh file
# use the first variable to file path
ENV_FILE="$1"

# file check
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: 파일 '$ENV_FILE' 가 존재하지 않습니다."
    exit 1
fi

# env path set
while read line; do
    export "$line"
done < "$ENV_FILE"

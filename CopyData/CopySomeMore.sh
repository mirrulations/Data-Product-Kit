filesOfInterest=(
    PACIFIC
    PBGC
    PBRB
    PC
    PCLOB
    PCSCOTUS
    PHMSA
    PHS
    PRC
    PRES
    PT
    PTO
    RATB
    RBS
    RHS
    RISC
    RITA
    RMA
    RRB
    RTB
    RUF
    RUS
    SAMHSA
)

for file in "${filesOfInterest[@]}"
do
    mkdir -p "mirrulations/$file"
done

# Copy the files
for file in "${filesOfInterest[@]}"
do
    aws s3 cp s3://mirror-aws-logs/mirrulations/$file/ mirrulations/$file/ --recursive
done


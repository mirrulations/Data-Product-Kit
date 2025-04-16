filesOfInterest(
SBA
SEC
SIGAR
SIGIR
SJI
SLSDC
SRBC
SS
SSA
SSS
STB
SWPA
TA
TRADE
TREAS
TSA
TTB
TVA
URMCC
USA
USAF
USAGM
USBC
USC
USCBP
USCC
USCG
USCIS
USDA
USDAIG
USEIB
USIP
USJC
USMINT
USN
USOPC
USPC
USPS
USSC
USTR
USUHS
VA
VCNP
VETS
WAPA
WCPO
WHD
)

for file in "${filesOfInterest[@]}"
do
    mkdir -p "mirrulations/$file"
done

# Copy the files
for file in "${filesOfInterest[@]}"
do
  aws s3 cp "s3://mirrulations/$file/" "mirrulations/$file" --recursive & disown
done

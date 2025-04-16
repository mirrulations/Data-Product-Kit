filesOfInterest=(
ETA
FAA
FAR
FAS
FASAB
FBI
FCA
FCC
FCIC
FCSC
FCSIC
FDA
FDIC
FEC
FEMA
FERC
FFIEC
FHFA
FHFB
FHWA
FINCEN
FINCIC
FIRSTNET
FISCAL
FLETC
FLRA
FMC
FMCS
FMCSA
FNS
FPAC
FPPO
FR
FRA
FRS
FRTIB
FS
FSA
FSIS
FSOC
FTA
FTC
FTZB
FWS
GAO
GAPFAC
GCERC
GEO
GIPSA
GPO
GSA
HHS
HHSIG
HOPE
HPAC
HRSA
HST
HUD
IAF
IAIA
ICEB
IHS
IIO
IPEC
IRS
ISOO
ITA
ITC
JBEA
LMSO
)

# Create the base directory if it does not exist
mkdir -p mirrulations

# Loop through each item in the array, create directories, and copy files
for file in "${filesOfInterest[@]}"; do
  mkdir -p "mirrulations/$file"
done

# Copy the files from S3
for file in "${filesOfInterest[@]}"; do
  aws s3 cp "s3://mirrulations/$file/" "mirrulations/$file" --recursive & disown
done
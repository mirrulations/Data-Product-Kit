filesOfInterest=(
LOC
LSC
MARAD
MBDA
MCC
MCRMC
MISS
MKU
MMC
MMS
MSHA
MSHFRC
MSPB
NAL
NARA
NASA
NASS
NCD
NCLIS
NCMNPS
NCPC
NCPPCC
NCS
NCUA
NEC
NEIGHBOR
NHTSA
NIFA
NIGC
NIH
NIL
NIST
NLRB
NMB
NNSA
NOAA
NPREC
NPS
NRC
NRCS
NRPC
NSA
NSCAI
NSF
NSPC
NTIA
NTSB
NWBC
NWTRB
OCC
ODNI
OEPNU
OFAC
OFCCP
OFHEO
OFPP
OFR
OJJDP
OJP
OMB
ONCD
ONDCP
ONHIR
ONRR
OPIC
OPM
OPPM
OSC
OSHA
OSHRC
OSM
OSTP
OTS
)


mkdir -p mirrulations

# Loop through each item in the array, create directories, and copy files
for file in "${filesOfInterest[@]}"; do
  mkdir -p "mirrulations/$file"
done

# Copy the files from S3
for file in "${filesOfInterest[@]}"; do
  aws s3 cp "s3://mirrulations/$file/" "mirrulations/$file" --recursive & disown
done
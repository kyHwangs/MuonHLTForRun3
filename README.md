
# CMS Run 3 Muon HLT

## CMSSW_12_3_X

### Setup
```shell
cmsrel CMSSW_12_3_0_pre4
cd CMSSW_12_3_0_pre4/src
cmsenv
git cms-init

git cms-merge-topic silviodonato:customizeHLTforRun3_v2
# NOTE: some customizers are already integrated or not compatible any more

# Add new training for inside-out seed cleaner
git clone -b dev https://github.com/wonpoint4/RecoMuon-TrackerSeedGenerator.git data_tmp
cp data_tmp/xgb_*.xml RecoMuon/TrackerSeedGenerator/data
rm -rf data_tmp

# Add muon customizers and compile
git clone https://github.com/khaosmos93/MuonHLTForRun3.git HLTrigger/Configuration/python/MuonHLTForRun3

scram b -j 8
```

### HLT menu for data
```shell
hltGetConfiguration /dev/CMSSW_12_3_0/GRun/V17 \
 --process MYHLT \
 --eras Run3 \
 --data --globaltag auto:run3_hlt \
 --prescale 2.0e34+ZB+HLTPhysics \
 --paths \
HLTriggerFirstPath,\
HLT_IsoMu*,\
HLT_Mu*,\
HLT_DoubleMu*,\
HLT_Dimuon*,\
HLT_OldMu100_v*,\
HLT_TkMu100_v*,\
HLT_PFMET120_PFMHT120_IDTight_v*,\
HLTriggerFinalPath,\
HLTAnalyzerEndpath \
 --customise \
HLTrigger/Configuration/customizeHLTforCMSSW.customiseFor2018Input,\
HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeMuonHLTForPatatrackWithIsoAndTriplets,\
HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeMuonHLTForPatatrackTkMu,\
HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeMuonHLTForPatatrackNoVtx,\
HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeMuonHLTForPatatrackOpenMu,\
HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeIOSeedingPatatrack,\
RecoMuon/TrackerSeedGenerator/customizeOIseeding.customizeOIseeding,\
HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.addHLTL1METTkMu50 \
 --input /store/data/Run2018D/EphemeralHLTPhysics1/RAW/v1/000/323/775/00000/0244D183-F28D-2741-9DBF-1638BEDC734E.root \
 --max-events 100 \
 --full --offline --no-output >hlt_muon_data.py
```

### HLT menu for MC
```shell
hltGetConfiguration /dev/CMSSW_12_3_0/GRun/V17 \
 --process MYHLT \
 --eras Run3 \
 --mc --globaltag auto:phase1_2021_realistic \
 --unprescale \
 --paths \
HLTriggerFirstPath,\
HLT_IsoMu*,\
HLT_Mu*,\
HLT_DoubleMu*,\
HLT_Dimuon*,\
HLT_OldMu100_v*,\
HLT_TkMu100_v*,\
HLT_PFMET120_PFMHT120_IDTight_v*,\
HLTriggerFinalPath,\
HLTAnalyzerEndpath \
 --customise \
HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeMuonHLTForPatatrackWithIsoAndTriplets,\
HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeMuonHLTForPatatrackTkMu,\
HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeMuonHLTForPatatrackNoVtx,\
HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeMuonHLTForPatatrackOpenMu,\
HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeIOSeedingPatatrack,\
RecoMuon/TrackerSeedGenerator/customizeOIseeding.customizeOIseeding,\
HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.addHLTL1METTkMu50 \
 --input /store/mc/Run3Summer21DRPremix/WprimeToMuNu_M-5000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/120X_mcRun3_2021_realistic_v6-v2/2550000/026722bd-ccc5-4da2-9295-13896532d7ab.root \
 --max-events 100 \
 --full --offline --no-output >hlt_muon_mc.py
````


## CMSSW_12_1_X

<details><summary> show </summary>
<p>

### Setup
```shell
cmsrel CMSSW_12_1_0_pre4
cd CMSSW_12_1_0_pre4/src
cmsenv
git cms-init

git cms-merge-topic 35237  # no need in >= CMSSW_12_1_0_pre5

git cms-addpkg RecoMuon/TrackerSeedGenerator
git clone -b dev https://github.com/wonpoint4/RecoMuon-TrackerSeedGenerator.git RecoMuon/TrackerSeedGenerator/data

git cms-addpkg HLTrigger/Configuration
git clone https://github.com/khaosmos93/MuonHLTForRun3.git HLTrigger/Configuration/python/MuonHLTForRun3

scram b -j 8
```
</p>
</details>


## CMSSW_12_0_X

<details><summary> show </summary>
<p>

### Setup
```shell
cmsrel CMSSW_12_0_1
cd CMSSW_12_0_1/src
cmsenv
git cms-init

git cms-addpkg RecoMuon/TrackerSeedGenerator
git clone -b v7Fast https://github.com/wonpoint4/RecoMuon-TrackerSeedGenerator.git RecoMuon/TrackerSeedGenerator/data

git cms-addpkg HLTrigger/Configuration
git clone https://github.com/khaosmos93/MuonHLTForRun3.git HLTrigger/Configuration/python/MuonHLTForRun3

scram b -j 8
```
</p>
</details>

## CMSSW_11_3_X

<details><summary> show </summary>
<p>

### Setup
```shell
cmsrel CMSSW_11_3_1_patch1
cd CMSSW_11_3_1_patch1/src
cmsenv
git cms-init

# For OI and IO seeding upgrades
git cms-merge-topic khaosmos93:CMSSW_11_3_1_patch1-MuonHLTForRun3
git clone https://github.com/cms-data/RecoMuon-TrackerSeedGenerator.git RecoMuon/TrackerSeedGenerator/data
cp /afs/cern.ch/user/j/jschulte/public/OIDNN/* RecoMuon/TrackerSeedGenerator/data

# Customizer for Muon HLT
git cms-addpkg HLTrigger/Configuration
git clone https://github.com/khaosmos93/MuonHLTForRun3.git HLTrigger/Configuration/python/MuonHLTForRun3

scram b -j 8
```

### Obtaining HLT menu
1. hltGetConfiguration
```shell
hltGetConfiguration /dev/CMSSW_11_3_0/GRun/V14 --type GRun \
--path HLTriggerFirstPath,HLT_IsoMu24_v*,HLT_Mu50_v*,HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v*,HLTriggerFinalPath,HLTAnalyzerEndpath \
--unprescale --cff >$CMSSW_BASE/src/HLTrigger/Configuration/python/HLT_MuonHLT_cff.py
```

2. cmsDriver
* Run 3 MC
```shell
cmsDriver.py hlt_muon \
--python_filename=hlt_muon_Run3_mc.py \
--step HLT:MuonHLT \
--process MYHLT --era=Run3 \
--mc --conditions=113X_mcRun3_2021_realistic_v10 \
--customise=HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeDoubleMuIsoFix \
--customise=HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeMuonHLTForDoubletRemoval \
--customise=HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeMuonHLTForCscSegment \
--customise=HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeMuonHLTForGEM \
--customise=HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizerFuncForMuonHLTSeeding \
--customise=RecoMuon/TrackerSeedGenerator/customizeOIseeding.customizeOIseeding \
--filein=/store/mc/Run3Winter21DRMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/FlatPU30to80FEVT_112X_mcRun3_2021_realistic_v16-v2/120003/e786c41e-21ba-489f-880c-42d0a248e59e.root \
-n 100 --no_output --no_exec
```

* 2018 data
```shell
cmsDriver.py hlt_muon \
--python_filename=hlt_muon_Run3_data.py \
--step HLT:MuonHLT \
--process MYHLT --era=Run3 \
--data --conditions=113X_dataRun3_HLT_v1 \
--customise=HLTrigger/Configuration/customizeHLTforCMSSW.customiseFor2018Input \
--customise=HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeDoubleMuIsoFix \
--customise=HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeMuonHLTForDoubletRemoval \
--customise=HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeMuonHLTForCscSegment \
--customise=HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizerFuncForMuonHLTSeeding \
--customise=RecoMuon/TrackerSeedGenerator/customizeOIseeding.customizeOIseeding \
--filein=/store/data/Run2018D/EphemeralHLTPhysics1/RAW/v1/000/323/775/00000/0244D183-F28D-2741-9DBF-1638BEDC734E.root \
-n 100 --no_output --no_exec
```

* optionally, add the following lines at the end of the configuration file to print out more info, e.g.
```python
cat << EOT >> hlt_muon_Run3_mc.py
process.options.wantSummary = cms.untracked.bool( True )
if 'MessageLogger' in process.__dict__:
    process.MessageLogger.TriggerSummaryProducerAOD = cms.untracked.PSet()
    process.MessageLogger.L1GtTrigReport = cms.untracked.PSet()
    process.MessageLogger.L1TGlobalSummary = cms.untracked.PSet()
    process.MessageLogger.HLTrigReport = cms.untracked.PSet()
    process.MessageLogger.FastReport = cms.untracked.PSet()
    process.MessageLogger.ThroughputService = cms.untracked.PSet()
    process.MessageLogger.cerr.FwkReport.reportEvery = 1000
EOT
```

</p>
</details>


## CMSSW_11_2_0 (without Patatrack)

<details><summary> show </summary>
<p>

### Setup
```shell
cmsrel CMSSW_11_2_0
cd CMSSW_11_2_0/src
cmsenv
git cms-init

# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideL1TStage2Instructions
git remote add cms-l1t-offline git@github.com:cms-l1t-offline/cmssw.git
git fetch cms-l1t-offline l1t-integration-CMSSW_11_2_0
git cms-merge-topic -u cms-l1t-offline:l1t-integration-v105.5
git cms-addpkg L1Trigger/Configuration
git cms-addpkg L1Trigger/L1TMuon
git clone https://github.com/cms-l1t-offline/L1Trigger-L1TMuon.git L1Trigger/L1TMuon/data
git cms-addpkg L1Trigger/L1TCalorimeter
git clone https://github.com/cms-l1t-offline/L1Trigger-L1TCalorimeter.git L1Trigger/L1TCalorimeter/data

git cms-checkdeps -A -a

# temporary fix to fill BMTF muons
git remote add panoskatsoulis https://github.com/panoskatsoulis/cmssw.git
git cms-merge-topic panoskatsoulis:fix_empty_bmtf_ntuples

# Customizer for Muon HLT
git cms-addpkg HLTrigger/Configuration
git clone https://github.com/khaosmos93/MuonHLTForRun3.git HLTrigger/Configuration/python/MuonHLTForRun3

scram b -j 8
```

### Obtaining HLT menu
1. hltGetConfiguration
```shell
hltGetConfiguration /dev/CMSSW_11_2_0/GRun --type GRun \
--path HLTriggerFirstPath,HLT_IsoMu24_v*,HLT_Mu50_v*,HLTriggerFinalPath,HLTAnalyzerEndpath \
--unprescale --cff >$CMSSW_BASE/src/HLTrigger/Configuration/python/HLT_MuonHLT_cff.py
```

2. cmsDriver
   * Run 3 MC
```shell
cmsDriver.py hlt_muon \
--python_filename=hlt_muon_Run3_mc.py \
--step RAW2DIGI,HLT:MuonHLT \
--process MYHLT --era=Run3 \
--mc --conditions=112X_mcRun3_2021_realistic_v15 \
--customise=L1Trigger/Configuration/customiseReEmul.L1TReEmulMCFromRAW \
--customise=L1Trigger/Configuration/customiseSettings.L1TSettingsToCaloParams_2018_v1_4 \
--customise=HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeMuonHLTForDoubletRemoval \
--customise=HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeMuonHLTForCscSegment \
--customise=HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeMuonHLTForGEM \
--filein=/store/mc/Run3Winter20DRMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/GEN-SIM-RAW/DRFlatPU30to80_110X_mcRun3_2021_realistic_v6-v2/230001/4A5403D5-F9A2-204D-ADA3-ABF92F6AA673.root \
-n 100 --no_output --no_exec
```
and manually modify
```python
process.GlobalTag = GlobalTag(process.GlobalTag, '112X_mcRun3_2021_realistic_v15', '')
```

to

```python
process.GlobalTag = GlobalTag(process.GlobalTag, '112X_mcRun3_2021_realistic_v15', '')

import os
base = os.environ["CMSSW_BASE"]
process.GlobalTag.toGet = cms.VPSet(
    cms.PSet(record = cms.string("GEMeMapRcd"),
        tag = cms.string("GEMeMapDummy"),
        connect = cms.string("sqlite_file:" + base + "/src/L1Trigger/Configuration/test/GEMeMapDummy.db")
    )
)
process.muonGEMDigis.useDBEMap = True
```

   * 2018 data
```shell
cmsDriver.py hlt_muon \
--python_filename=hlt_muon_Run3_data.py \
--step HLT:MuonHLT \
--process MYHLT --era=Run3 \
--data --conditions=auto:run3_data_GRun \
--customise=HLTrigger/Configuration/customizeHLTforCMSSW.customisePixelGainForRun2Input \
--customise=HLTrigger/Configuration/customizeHLTforCMSSW.synchronizeHCALHLTofflineRun3on2018data \
--customise=HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeMuonHLTForDoubletRemoval \
--customise=HLTrigger/Configuration/MuonHLTForRun3/customizeMuonHLTForRun3.customizeMuonHLTForCscSegment \
--filein=/store/data/Run2018D/EphemeralHLTPhysics1/RAW/v1/000/323/775/00000/0244D183-F28D-2741-9DBF-1638BEDC734E.root \
-n 100 --no_output --no_exec
```

   * optionally, add the following lines at the end of the configuration file
```python
process.options.wantSummary = cms.untracked.bool( True )
if 'MessageLogger' in process.__dict__:
    process.MessageLogger.categories.append('TriggerSummaryProducerAOD')
    process.MessageLogger.categories.append('L1GtTrigReport')
    process.MessageLogger.categories.append('L1TGlobalSummary')
    process.MessageLogger.categories.append('HLTrigReport')
    process.MessageLogger.categories.append('FastReport')
    process.MessageLogger.cerr.FwkReport.reportEvery = 1000
```

</p>
</details>


import FWCore.ParameterSet.Config as cms

from HLTrigger.Configuration.common import *

def customizeIOSeedingPatatrack_v3(
        process, newProcessName = "MYHLT",
        doSort = False,
        nSeedsMaxBs = (99999, 99999), nSeedsMaxEs = (99999, 99999),
        mvaCutBs = (0.04, 0.04), mvaCutEs = (0.04, 0.04)):

        if not hasattr(process, "HLTIterativeTrackingIteration0ForIterL3Muon") or\
           not hasattr(process, "HLTIterativeTrackingIteration0ForIterL3FromL1Muon"):
                return process

        import HLTrigger.Configuration.MuonHLTForRun3.mvaScale as _mvaScale

        # -- Seed MVA Classifiers
        process.hltIter0IterL3MuonPixelSeedsFromPixelTracksFiltered = cms.EDProducer("MuonHLTSeedMVAClassifier",
                rejectAll = cms.bool(False),
                isFromL1 = cms.bool(False),

                src    = cms.InputTag("hltIter0IterL3MuonPixelSeedsFromPixelTracks"),
                L1Muon = cms.InputTag("hltGtStage2Digis", "Muon"),
                L2Muon = cms.InputTag("hltL2MuonCandidates", ""),

                mvaFileBL1 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/xgb_Run3_Iter0FromL1_PatatrackSeeds_barrel_v3.xml"),
                mvaFileEL1 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/xgb_Run3_Iter0FromL1_PatatrackSeeds_endcap_v3.xml"),

                mvaScaleMeanBL1 = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0FromL1_PatatrackSeeds_barrel_v3_ScaleMean") ),
                mvaScaleStdBL1  = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0FromL1_PatatrackSeeds_barrel_v3_ScaleStd") ),
                mvaScaleMeanEL1 = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0FromL1_PatatrackSeeds_endcap_v3_ScaleMean") ),
                mvaScaleStdEL1  = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0FromL1_PatatrackSeeds_endcap_v3_ScaleStd") ),

                mvaFileBL2 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/xgb_Run3_Iter0_PatatrackSeeds_barrel_v3.xml"),
                mvaFileEL2 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/xgb_Run3_Iter0_PatatrackSeeds_endcap_v3.xml"),

                mvaScaleMeanBL2 = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0_PatatrackSeeds_barrel_v3_ScaleMean") ),
                mvaScaleStdBL2  = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0_PatatrackSeeds_barrel_v3_ScaleStd") ),
                mvaScaleMeanEL2 = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0_PatatrackSeeds_endcap_v3_ScaleMean") ),
                mvaScaleStdEL2  = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0_PatatrackSeeds_endcap_v3_ScaleStd") ),

                doSort = cms.bool(doSort),
                nSeedsMaxB = cms.int32(nSeedsMaxBs[1]),
                nSeedsMaxE = cms.int32(nSeedsMaxEs[1]),

                mvaCutB = cms.double(mvaCutBs[1]),
                mvaCutE = cms.double(mvaCutEs[1])
        )
        process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksFiltered = cms.EDProducer("MuonHLTSeedMVAClassifier",
                rejectAll = cms.bool(False),
                isFromL1 = cms.bool(True),

                src    = cms.InputTag("hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks"),
                L1Muon = cms.InputTag("hltGtStage2Digis", "Muon"),
                L2Muon = cms.InputTag("hltL2MuonCandidates", ""),

                mvaFileBL1 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/xgb_Run3_Iter0FromL1_PatatrackSeeds_barrel_v3.xml"),
                mvaFileEL1 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/xgb_Run3_Iter0FromL1_PatatrackSeeds_endcap_v3.xml"),

                mvaScaleMeanBL1 = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0FromL1_PatatrackSeeds_barrel_v3_ScaleMean") ),
                mvaScaleStdBL1  = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0FromL1_PatatrackSeeds_barrel_v3_ScaleStd") ),
                mvaScaleMeanEL1 = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0FromL1_PatatrackSeeds_endcap_v3_ScaleMean") ),
                mvaScaleStdEL1  = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0FromL1_PatatrackSeeds_endcap_v3_ScaleStd") ),

                mvaFileBL2 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/xgb_Run3_Iter0_PatatrackSeeds_barrel_v3.xml"),
                mvaFileEL2 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/xgb_Run3_Iter0_PatatrackSeeds_endcap_v3.xml"),

                mvaScaleMeanBL2 = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0_PatatrackSeeds_barrel_v3_ScaleMean") ),
                mvaScaleStdBL2  = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0_PatatrackSeeds_barrel_v3_ScaleStd") ),
                mvaScaleMeanEL2 = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0_PatatrackSeeds_endcap_v3_ScaleMean") ),
                mvaScaleStdEL2  = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0_PatatrackSeeds_endcap_v3_ScaleStd") ),

                doSort = cms.bool(doSort),
                nSeedsMaxB = cms.int32(nSeedsMaxBs[1]),
                nSeedsMaxE = cms.int32(nSeedsMaxEs[1]),

                mvaCutB = cms.double(mvaCutBs[1]),
                mvaCutE = cms.double(mvaCutEs[1])
        )

        return process

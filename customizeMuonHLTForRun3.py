import FWCore.ParameterSet.Config as cms

from HLTrigger.Configuration.common import *

def enableDoubletRecoveryInMuon(process):

    if not hasattr(process, "HLTIterativeTrackingDoubletRecovery"):
        return process

    # IO from L2



    # IO from L1



    # without ROI - just use tracks from the Doublet Recovery -> almost no timing increase? or maybe in MuonProducer?
    process.hltIterL3MuonAndMuonFromL1AndDoubletRecoveryMerged = cms.EDProducer( "TrackListMerger",
        ShareFrac = cms.double( 0.19 ),
        FoundHitBonus = cms.double( 5.0 ),
        LostHitPenalty = cms.double( 20.0 ),
        MinPT = cms.double( 0.05 ),
        Epsilon = cms.double( -0.001 ),
        MaxNormalizedChisq = cms.double( 1000.0 ),
        MinFound = cms.int32( 3 ),
        TrackProducers = cms.VInputTag( 'hltIterL3MuonAndMuonFromL1Merged','hltDoubletRecoveryPFlowTrackSelectionHighPurity' ),
        hasSelector = cms.vint32( 0, 0 ),
        indivShareFrac = cms.vdouble( 1.0, 1.0 ),
        selectedTrackQuals = cms.VInputTag( 'hltIterL3MuonAndMuonFromL1Merged','hltDoubletRecoveryPFlowTrackSelectionHighPurity' ),
        setsToMerge = cms.VPSet(
          cms.PSet(  pQual = cms.bool( False ),
            tLists = cms.vint32( 0, 1 )
          )
        ),
        trackAlgoPriorityOrder = cms.string( "hltESPTrackAlgoPriorityOrder" ),
        allowFirstHitShare = cms.bool( True ),
        newQuality = cms.string( "confirmed" ),
        copyExtras = cms.untracked.bool( True ),
        writeOnlyTrkQuals = cms.bool( False ),
        copyMVA = cms.bool( False )
    )

    process.hltIterL3GlbMuon.L3TrajBuilderParameters.tkTrajLabel =  cms.InputTag( "hltIterL3MuonAndMuonFromL1AndDoubletRecoveryMerged" )
    process.hltIterL3MuonsNoID.inputCollectionLabels = cms.VInputTag( 'hltIterL3MuonAndMuonFromL1AndDoubletRecoveryMerged','hltIterL3GlbMuon','hltL2Muons:UpdatedAtVtx' )
    process.hltIterL3MuonTracks.track = cms.InputTag( "hltIterL3MuonAndMuonFromL1AndDoubletRecoveryMerged" )

    process.HLTL3muonrecoNocandSequence = cms.Sequence(
        process.HLTIterL3muonTkCandidateSequence +
        process.hltIterL3MuonMerged +
        process.hltIterL3MuonAndMuonFromL1Merged +
        process.hltIterL3MuonAndMuonFromL1AndDoubletRecoveryMerged + ## HERE
        process.hltIterL3GlbMuon +
        process.hltIterL3MuonsNoID +
        process.hltIterL3Muons +
        process.hltL3MuonsIterL3Links +
        process.hltIterL3MuonTracks
    )

    process.HLTIterL3muonTkCandidateSequence = cms.Sequence(
        process.HLTDoLocalPixelSequence +
        process.HLTDoLocalStripSequence +
        process.HLTIterativeTrackingIteration0 + ## HERE
        process.HLTIterativeTrackingDoubletRecovery + ## HERE
        process.HLTIterL3OIAndIOFromL2muonTkCandidateSequence +
        process.hltL1MuonsPt0 +
        process.HLTIterL3IOmuonFromL1TkCandidateSequence
    )

    return process


## To-do
# Timing comparison : Using ROI vs. not using ROI - don't need to do trajectory building, but maybe more consuming at hltIterL3GlbMuon?
# Are there any ROI modules in cms-sw that selecting trks, instead of PixelSeeds?

# Further check is needed if our changes proppagate to all relavant muon Paths such as displacedMuons, etc...
# Add Doublet Recovery in trk iso in IsoMu24
# Synchronize trk selection of IO and PF Tracking
# If needed, new IO BDT training using "the extended Patatrack pixeltracks"
def customizeIOSeedingPatatrack_v4(
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

import FWCore.ParameterSet.Config as cms

from HLTrigger.Configuration.common import *

def enableDoubletRecoveryInIOFromL1(process):

    # IO from L1 - Iter3FromL1
    process.hltIter3IterL3FromL1MuonClustersRefRemoval = cms.EDProducer( "TrackClusterRemover",
        trajectories = cms.InputTag( "hltIter0IterL3FromL1MuonTrackSelectionHighPurity" ), ## HERE
        trackClassifier = cms.InputTag( '','QualityMasks' ),
        pixelClusters = cms.InputTag( "hltSiPixelClusters" ),
        stripClusters = cms.InputTag( "hltSiStripRawToClustersFacility" ),
        oldClusterRemovalInfo = cms.InputTag( "" ),
        TrackQuality = cms.string( "highPurity" ),
        maxChi2 = cms.double( 16.0 ),
        minNumberOfLayersWithMeasBeforeFiltering = cms.int32( 0 ),
        overrideTrkQuals = cms.InputTag( "" )
    )

    process.hltIter3IterL3FromL1MuonMaskedMeasurementTrackerEvent = cms.EDProducer( "MaskedMeasurementTrackerEventProducer",
    src = cms.InputTag( "hltMeasurementTrackerEvent" ),
    OnDemand = cms.bool( False ),
    clustersToSkip = cms.InputTag( "hltIter3IterL3FromL1MuonClustersRefRemoval" )
    )

    process.hltIter3IterL3FromL1MuonPixelLayersAndRegions = cms.EDProducer( "PixelInactiveAreaTrackingRegionsSeedingLayersProducer",
    RegionPSet = cms.PSet(
      vertexCollection = cms.InputTag( "hltTrimmedPixelVertices" ),
      beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
      zErrorBeamSpot = cms.double( 15.0 ),
      extraPhi = cms.double( 0.0 ),
      extraEta = cms.double( 0.0 ),
      maxNVertices = cms.int32( 3 ),
      nSigmaZVertex = cms.double( 3.0 ),
      nSigmaZBeamSpot = cms.double( 4.0 ),
      ptMin = cms.double( 1.2 ),
      operationMode = cms.string( "VerticesFixed" ),
      searchOpt = cms.bool( False ),
      whereToUseMeasurementTracker = cms.string( "ForSiStrips" ),
      originRadius = cms.double( 0.015 ),
      measurementTrackerName = cms.InputTag( "hltIter3IterL3FromL1MuonMaskedMeasurementTrackerEvent" ),
      precise = cms.bool( True ),
      zErrorVertex = cms.double( 0.03 )
    ),
    inactivePixelDetectorLabels = cms.VInputTag( 'hltSiPixelDigis' ),
    badPixelFEDChannelCollectionLabels = cms.VInputTag( 'hltSiPixelDigis' ),
    ignoreSingleFPixPanelModules = cms.bool( True ),
    debug = cms.untracked.bool( False ),
    createPlottingFiles = cms.untracked.bool( False ),
    layerList = cms.vstring( 'BPix1+BPix2',
      'BPix2+FPix1_pos',
      'BPix2+FPix1_neg',
      'FPix1_pos+FPix2_pos',
      'FPix1_neg+FPix2_neg' ),
    BPix = cms.PSet(
      hitErrorRPhi = cms.double( 0.0027 ),
      TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
      skipClusters = cms.InputTag( "hltIter3IterL3FromL1MuonClustersRefRemoval" ),
      useErrorsFromParam = cms.bool( True ),
      hitErrorRZ = cms.double( 0.006 ),
      HitProducer = cms.string( "hltSiPixelRecHits" )
    ),
    FPix = cms.PSet(
      hitErrorRPhi = cms.double( 0.0051 ),
      TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
      skipClusters = cms.InputTag( "hltIter3IterL3FromL1MuonClustersRefRemoval" ),
      useErrorsFromParam = cms.bool( True ),
      hitErrorRZ = cms.double( 0.0036 ),
      HitProducer = cms.string( "hltSiPixelRecHits" )
    ),
    TIB = cms.PSet(  ),
    TID = cms.PSet(  ),
    TOB = cms.PSet(  ),
    TEC = cms.PSet(  ),
    MTIB = cms.PSet(  ),
    MTID = cms.PSet(  ),
    MTOB = cms.PSet(  ),
    MTEC = cms.PSet(  )
    )

    ## pt-dep ROI - from Run3 (hltIterL3FromL1MuonPixelTracksTrackingRegions)
    process.hltIter3IterL3FromL1MuonTrackingRegions = cms.EDProducer( "L1MuonSeededTrackingRegionsEDProducer",
    Propagator = cms.string( "SteppingHelixPropagatorAny" ),
    L1MinPt = cms.double( 0.0 ),
    L1MaxEta = cms.double( 2.5 ),
    L1MinQuality = cms.uint32( 7 ),
    SetMinPtBarrelTo = cms.double( 3.5 ),
    SetMinPtEndcapTo = cms.double( 1.0 ),
    CentralBxOnly = cms.bool( True ),
    RegionPSet = cms.PSet(
      vertexCollection = cms.InputTag( "hltTrimmedPixelVertices" ), # HERE
      deltaEtas = cms.vdouble( 0.175, 0.175, 0.175, 0.175 ), # HERE
      beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
      zErrorBeamSpot = cms.double( 15.0 ), # HERE
      maxNVertices = cms.int32( 3 ), # HERE
      maxNRegions = cms.int32( 3 ), # HERE
      nSigmaZVertex = cms.double( 3.0 ),
      nSigmaZBeamSpot = cms.double( 4.0 ),
      ptMin = cms.double( 1.2 ), # HERE
      mode = cms.string( "VerticesFixed" ), # HERE
      input = cms.InputTag( "hltL1MuonsPt0" ),
      ptRanges = cms.vdouble( 0.0, 10.0, 15.0, 20.0, 1.0E64 ),
      searchOpt = cms.bool( False ),
      deltaPhis = cms.vdouble( 0.5, 0.4, 0.3, 0.15 ),  # HERE
      whereToUseMeasurementTracker = cms.string( "ForSiStrips" ), # HERE
      originRadius = cms.double( 0.015 ), # HERE
      measurementTrackerName = cms.InputTag( "hltIter3IterL3FromL1MuonMaskedMeasurementTrackerEvent" ), # HERE
      precise = cms.bool( True )
    ),
    ServiceParameters = cms.PSet(
      RPCLayers = cms.bool( True ),
      UseMuonNavigation = cms.untracked.bool( True ),
      Propagators = cms.untracked.vstring( 'SteppingHelixPropagatorAny' )
    )
    )

    process.hltIter3IterL3FromL1MuonPixelClusterCheck = cms.EDProducer( "ClusterCheckerEDProducer",
    doClusterCheck = cms.bool( False ),
    MaxNumberOfStripClusters = cms.uint32( 50000 ),
    ClusterCollectionLabel = cms.InputTag( "hltMeasurementTrackerEvent" ),
    MaxNumberOfPixelClusters = cms.uint32( 40000 ),
    PixelClusterCollectionLabel = cms.InputTag( "hltSiPixelClusters" ),
    cut = cms.string( "" ),
    silentClusterCheck = cms.untracked.bool( False )
    )

    process.hltIter3IterL3FromL1MuonPixelHitDoublets = cms.EDProducer( "HitPairEDProducer",
    seedingLayers = cms.InputTag( "hltIter3IterL3FromL1MuonPixelLayersAndRegions" ), ## HERE
    trackingRegions = cms.InputTag( "hltIter3IterL3FromL1MuonTrackingRegions" ), ## HERE
    trackingRegionsSeedingLayers = cms.InputTag( "" ), ## HERE
    clusterCheck = cms.InputTag( "hltIter3IterL3FromL1MuonPixelClusterCheck" ),
    produceSeedingHitSets = cms.bool( True ),
    produceIntermediateHitDoublets = cms.bool( False ),
    maxElement = cms.uint32( 0 ),
    maxElementTotal = cms.uint32( 50000000 ),
    putEmptyIfMaxElementReached = cms.bool( False ),
    layerPairs = cms.vuint32( 0 )
    )

    process.hltIter3IterL3FromL1MuonPixelSeeds = cms.EDProducer( "SeedCreatorFromRegionConsecutiveHitsEDProducer",
    seedingHitSets = cms.InputTag( "hltIter3IterL3FromL1MuonPixelHitDoublets" ),
    propagator = cms.string( "PropagatorWithMaterialParabolicMf" ),
    SeedMomentumForBOFF = cms.double( 5.0 ),
    OriginTransverseErrorMultiplier = cms.double( 1.0 ),
    MinOneOverPtError = cms.double( 1.0 ),
    TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
    magneticField = cms.string( "ParabolicMf" ),
    forceKinematicWithRegionDirection = cms.bool( False ),
    SeedComparitorPSet = cms.PSet(  ComponentName = cms.string( "none" ) )
    )

    process.hltIter3IterL3FromL1MuonCkfTrackCandidates = cms.EDProducer( "CkfTrackCandidateMaker",
    cleanTrajectoryAfterInOut = cms.bool( False ),
    doSeedingRegionRebuilding = cms.bool( False ),
    onlyPixelHitsForSeedCleaner = cms.bool( False ),
    reverseTrajectories = cms.bool( False ),
    useHitsSplitting = cms.bool( False ),
    MeasurementTrackerEvent = cms.InputTag( "hltIter3IterL3FromL1MuonMaskedMeasurementTrackerEvent" ),
    src = cms.InputTag( "hltIter3IterL3FromL1MuonPixelSeeds" ),
    clustersToSkip = cms.InputTag( "" ),
    phase2clustersToSkip = cms.InputTag( "" ),
    TrajectoryBuilderPSet = cms.PSet(  refToPSet_ = cms.string( "HLTIter2GroupedCkfTrajectoryBuilderIT" ) ),
    TransientInitialStateEstimatorParameters = cms.PSet(
      propagatorAlongTISE = cms.string( "PropagatorWithMaterialParabolicMf" ),
      numberMeasurementsForFit = cms.int32( 4 ),
      propagatorOppositeTISE = cms.string( "PropagatorWithMaterialParabolicMfOpposite" )
    ),
    numHitsForSeedCleaner = cms.int32( 4 ),
    NavigationSchool = cms.string( "SimpleNavigationSchool" ),
    RedundantSeedCleaner = cms.string( "CachingSeedCleanerBySharedInput" ),
    TrajectoryCleaner = cms.string( "hltESPTrajectoryCleanerBySharedHits" ),
    maxNSeeds = cms.uint32( 100000 ),
    maxSeedsBeforeCleaning = cms.uint32( 1000 )
    )

    process.hltIter3IterL3FromL1MuonCtfWithMaterialTracks = cms.EDProducer( "TrackProducer",
    useSimpleMF = cms.bool( True ),
    SimpleMagneticField = cms.string( "ParabolicMf" ),
    src = cms.InputTag( "hltIter3IterL3FromL1MuonCkfTrackCandidates" ),
    clusterRemovalInfo = cms.InputTag( "" ),
    beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
    Fitter = cms.string( "hltESPFittingSmootherIT" ),
    useHitsSplitting = cms.bool( False ),
    alias = cms.untracked.string( "ctfWithMaterialTracks" ),
    TrajectoryInEvent = cms.bool( False ),
    TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
    AlgorithmName = cms.string( "hltIter3IterL3FromL1Muon" ),
    Propagator = cms.string( "hltESPRungeKuttaTrackerPropagator" ),
    GeometricInnerState = cms.bool( True ),
    NavigationSchool = cms.string( "" ),
    MeasurementTracker = cms.string( "" ),
    MeasurementTrackerEvent = cms.InputTag( "hltIter3IterL3FromL1MuonMaskedMeasurementTrackerEvent" )
    )

    process.hltIter3IterL3FromL1MuonTrackCutClassifier = cms.EDProducer( "TrackCutClassifier",
    src = cms.InputTag( "hltIter3IterL3FromL1MuonCtfWithMaterialTracks" ),
    beamspot = cms.InputTag( "hltOnlineBeamSpot" ),
    vertices = cms.InputTag( "hltTrimmedPixelVertices" ),
    ignoreVertices = cms.bool( False ),
    qualityCuts = cms.vdouble( -0.7, 0.1, 0.7 ),
    mva = cms.PSet(
      minPixelHits = cms.vint32( 0, 0, 0 ),
      maxDzWrtBS = cms.vdouble( 3.40282346639E38, 24.0, 15.0 ),
      dr_par = cms.PSet(
        d0err = cms.vdouble( 0.003, 0.003, 0.003 ),
        dr_par2 = cms.vdouble( 3.40282346639E38, 0.3, 0.3 ),
        dr_par1 = cms.vdouble( 3.40282346639E38, 0.4, 0.4 ),
        dr_exp = cms.vint32( 4, 4, 4 ),
        d0err_par = cms.vdouble( 0.001, 0.001, 0.001 )
      ),
      maxLostLayers = cms.vint32( 1, 1, 1 ),
      min3DLayers = cms.vint32( 0, 0, 0 ),
      dz_par = cms.PSet(
        dz_par1 = cms.vdouble( 3.40282346639E38, 0.4, 0.4 ),
        dz_par2 = cms.vdouble( 3.40282346639E38, 0.35, 0.35 ),
        dz_exp = cms.vint32( 4, 4, 4 )
      ),
      minNVtxTrk = cms.int32( 3 ),
      maxDz = cms.vdouble( 0.5, 0.2, 3.40282346639E38 ),
      minNdof = cms.vdouble( 1.0E-5, 1.0E-5, 1.0E-5 ),
      maxChi2 = cms.vdouble( 9999.0, 25.0, 16.0 ),
      maxChi2n = cms.vdouble( 1.2, 1.0, 0.7 ),
      maxDr = cms.vdouble( 0.5, 0.03, 3.40282346639E38 ),
      minLayers = cms.vint32( 3, 3, 3 )
    )
    )

    process.hltIter3IterL3FromL1MuonTrackSelectionHighPurity = cms.EDProducer( "TrackCollectionFilterCloner",
    originalSource = cms.InputTag( "hltIter3IterL3FromL1MuonCtfWithMaterialTracks" ),
    originalMVAVals = cms.InputTag( 'hltIter3IterL3FromL1MuonTrackCutClassifier','MVAValues' ),
    originalQualVals = cms.InputTag( 'hltIter3IterL3FromL1MuonTrackCutClassifier','QualityMasks' ),
    minQuality = cms.string( "highPurity" ),
    copyExtras = cms.untracked.bool( True ),
    copyTrajectories = cms.untracked.bool( False )
    )

    ## New track merger
    process.hltIter03IterL3FromL1MuonMerged  = cms.EDProducer( "TrackListMerger",
        ShareFrac = cms.double( 0.19 ),
        FoundHitBonus = cms.double( 5.0 ),
        LostHitPenalty = cms.double( 20.0 ),
        MinPT = cms.double( 0.05 ),
        Epsilon = cms.double( -0.001 ),
        MaxNormalizedChisq = cms.double( 1000.0 ),
        MinFound = cms.int32( 3 ),
        TrackProducers = cms.VInputTag( 'hltIter0IterL3FromL1MuonTrackSelectionHighPurity','hltIter3IterL3FromL1MuonTrackSelectionHighPurity' ),
        hasSelector = cms.vint32( 0, 0 ),
        indivShareFrac = cms.vdouble( 1.0, 1.0 ),
        selectedTrackQuals = cms.VInputTag( 'hltIter0IterL3FromL1MuonTrackSelectionHighPurity','hltIter3IterL3FromL1MuonTrackSelectionHighPurity' ),
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

    process.hltIterL3MuonAndMuonFromL1Merged.TrackProducers = cms.VInputTag( 'hltIterL3MuonMerged','hltIter03IterL3FromL1MuonMerged' )
    process.hltIterL3MuonAndMuonFromL1Merged.selectedTrackQuals = cms.VInputTag( 'hltIterL3MuonMerged','hltIter03IterL3FromL1MuonMerged' )
    process.hltIterL3MuonsNoID.TrackExtractorPSet.inputTrackCollection = cms.InputTag( "hltIter03IterL3FromL1MuonMerged" )

    process.HLTIterativeTrackingIteration3ForIterL3FromL1Muon = cms.Sequence(
        process.hltIter3IterL3FromL1MuonClustersRefRemoval +
        process.hltIter3IterL3FromL1MuonMaskedMeasurementTrackerEvent +
        process.hltIter3IterL3FromL1MuonPixelLayersAndRegions +
        process.hltIter3IterL3FromL1MuonTrackingRegions + # HERE
        process.hltIter3IterL3FromL1MuonPixelClusterCheck +
        process.hltIter3IterL3FromL1MuonPixelHitDoublets +
        process.hltIter3IterL3FromL1MuonPixelSeeds +
        process.hltIter3IterL3FromL1MuonCkfTrackCandidates +
        process.hltIter3IterL3FromL1MuonCtfWithMaterialTracks +
        process.hltIter3IterL3FromL1MuonTrackCutClassifier +
        process.hltIter3IterL3FromL1MuonTrackSelectionHighPurity
    )

    process.HLTIterL3IOmuonFromL1TkCandidateSequence = cms.Sequence(
        process.HLTRecopixelvertexingSequenceForIterL3FromL1Muon +
        process.HLTIterativeTrackingIteration0ForIterL3FromL1Muon +
        process.HLTIterativeTrackingIteration3ForIterL3FromL1Muon ## HERE
    )

    process.HLTL3muonrecoNocandSequence = cms.Sequence(
        process.HLTIterL3muonTkCandidateSequence +
        process.hltIter03IterL3FromL1MuonMerged + ## HERE
        process.hltIterL3MuonMerged +
        process.hltIterL3MuonAndMuonFromL1Merged +
        process.hltIterL3GlbMuon +
        process.hltIterL3MuonsNoID +
        process.hltIterL3Muons +
        process.hltL3MuonsIterL3Links +
        process.hltIterL3MuonTracks
    )

    return process


## To-do
# Timing comparison : Using ROI vs. not using ROI - don't need to do trajectory building, but maybe more consuming at hltIterL3GlbMuon?
# Are there any ROI modules in cms-sw that selecting trks, instead of PixelSeeds?

# Further check is needed if our changes proppagate to all relavant muon Paths such as displacedMuons, etc...
# Add Doublet Recovery in trk iso in IsoMu24
# Synchronize trk selection of IO and PF Tracking
# If needed, new IO BDT training using "the extended Patatrack pixeltracks"

def enableFullIter3FromL1(process):

    if not hasattr(process, "hltIter3IterL3FromL1MuonPixelLayersAndRegions"):
        return process

    process.hltIter3IterL3FromL1MuonPixelLayersAndRegions.layerList = cms.vstring( 'BPix1+BPix2',
      'BPix1+BPix3',
      'BPix1+BPix4',
      'BPix2+BPix3',
      'BPix2+BPix4',
      'BPix3+BPix4',
      'BPix1+FPix1_pos',
      'BPix1+FPix1_neg',
      'BPix1+FPix2_pos',
      'BPix1+FPix2_neg',
      'BPix1+FPix3_pos',
      'BPix1+FPix3_neg',
      'BPix2+FPix1_pos',
      'BPix2+FPix1_neg',
      'BPix2+FPix2_pos',
      'BPix2+FPix2_neg',
      'BPix3+FPix1_pos',
      'BPix3+FPix1_neg',
      'FPix1_pos+FPix2_pos',
      'FPix1_neg+FPix2_neg',
      'FPix1_pos+FPix3_pos',
      'FPix1_neg+FPix3_neg',
      'FPix2_pos+FPix3_pos',
      'FPix2_neg+FPix3_neg' )

    process.hltIter3IterL3FromL1MuonTrackingRegions.RegionPSet.deltaEtas = cms.vdouble( 0.35, 0.35, 0.35, 0.35 )
    process.hltIter3IterL3FromL1MuonTrackingRegions.RegionPSet.deltaPhis = cms.vdouble( 1.0, 0.8, 0.6, 0.3 )
    #process.hltIter3IterL3FromL1MuonTrackingRegions.RegionPSet.maxNRegions = cms.int32( 5 )

    return process

# To maximize the signal seeds of Iter3FromL1, only for training
def disableClustersRefRemoval(process):

    if not hasattr(process, "hltIter3IterL3FromL1MuonClustersRefRemoval"):
        return process

    process.hltIter3IterL3FromL1MuonPixelLayersAndRegions.RegionPSet.measurementTrackerName = cms.InputTag( "hltMeasurementTrackerEvent" )
    process.hltIter3IterL3FromL1MuonPixelLayersAndRegions.BPix = cms.PSet(
      hitErrorRPhi = cms.double( 0.0027 ),
      TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
      #skipClusters = cms.InputTag( "hltIter3IterL3FromL1MuonClustersRefRemoval" ),
      useErrorsFromParam = cms.bool( True ),
      hitErrorRZ = cms.double( 0.006 ),
      HitProducer = cms.string( "hltSiPixelRecHits" )
    )
    process.hltIter3IterL3FromL1MuonPixelLayersAndRegions.FPix = cms.PSet(
      hitErrorRPhi = cms.double( 0.0051 ),
      TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
      #skipClusters = cms.InputTag( "hltIter3IterL3FromL1MuonClustersRefRemoval" ),
      useErrorsFromParam = cms.bool( True ),
      hitErrorRZ = cms.double( 0.0036 ),
      HitProducer = cms.string( "hltSiPixelRecHits" )
    )
    process.hltIter3IterL3FromL1MuonTrackingRegions.RegionPSet.measurementTrackerName = cms.InputTag( "hltMeasurementTrackerEvent" )
    process.hltIter3IterL3FromL1MuonCkfTrackCandidates.MeasurementTrackerEvent = cms.InputTag( "hltMeasurementTrackerEvent" )
    process.hltIter3IterL3FromL1MuonCtfWithMaterialTracks.MeasurementTrackerEvent = cms.InputTag( "hltMeasurementTrackerEvent" )
    process.HLTIterativeTrackingIteration3ForIterL3FromL1Muon = cms.Sequence(
        #process.hltIter3IterL3FromL1MuonClustersRefRemoval +
        #process.hltIter3IterL3FromL1MuonMaskedMeasurementTrackerEvent +
        process.hltIter3IterL3FromL1MuonPixelLayersAndRegions +
        process.hltIter3IterL3FromL1MuonTrackingRegions + # HERE
        process.hltIter3IterL3FromL1MuonPixelClusterCheck +
        process.hltIter3IterL3FromL1MuonPixelHitDoublets +
        process.hltIter3IterL3FromL1MuonPixelSeeds +
        process.hltIter3IterL3FromL1MuonCkfTrackCandidates +
        process.hltIter3IterL3FromL1MuonCtfWithMaterialTracks +
        process.hltIter3IterL3FromL1MuonTrackCutClassifier +
        process.hltIter3IterL3FromL1MuonTrackSelectionHighPurity
    )

    return process

def disablePixelHitsOI(process):

    if not hasattr(process, "hltIterL3OIMuonTrackCutClassifier"):
        return process

    process.hltIterL3OIMuonTrackCutClassifier.mva.minPixelHits = cms.vint32(0, 0, 0)
    process.hltIterL3OIMuonTrackCutClassifier.mva.min3DLayers = cms.vint32(0, 0, 0)

    if not hasattr(process, "hltIterL3OIMuonTrackCutClassifierCPUOnly"):
        return process

    process.hltIterL3OIMuonTrackCutClassifierCPUOnly.mva.minPixelHits = cms.vint32(0, 0, 0)
    process.hltIterL3OIMuonTrackCutClassifierCPUOnly.mva.min3DLayers = cms.vint32(0, 0, 0)

    return process

def enableChainingIOfromL1(process):

    process.hltIterL3MuonL1MuonNoL2Selector = cms.EDProducer( "HLTL1MuonNoL2Selector",
      InputObjects = cms.InputTag( 'hltGtStage2Digis','Muon' ),
      L2CandTag = cms.InputTag( "hltL2MuonCandidates" ),
      SeedMapTag = cms.InputTag( "hltL2Muons" ),
      L1MinPt = cms.double( -1.0 ),
      L1MaxEta = cms.double( 5.0 ),
      L1MinQuality = cms.uint32( 7 ),
      CentralBxOnly = cms.bool( True )
    )
    process.hltIterL3FromL1MuonPixelTracksTrackingRegions.RegionPSet.input = cms.InputTag( "hltIterL3MuonL1MuonNoL2Selector" )

    if hasattr(process, "hltIter3IterL3FromL1MuonTrackingRegions"):
        process.hltIter3IterL3FromL1MuonTrackingRegions.RegionPSet.input = cms.InputTag( "hltIterL3MuonL1MuonNoL2Selector" )

    process.HLTIterL3muonTkCandidateSequence = cms.Sequence(
        process.HLTDoLocalPixelSequence +
        process.HLTDoLocalStripSequence +
        process.HLTIterL3OIAndIOFromL2muonTkCandidateSequence +
        process.hltL1MuonsPt0 +
        process.hltIterL3MuonL1MuonNoL2Selector + # HERE
        process.HLTIterL3IOmuonFromL1TkCandidateSequence
    )

    ## CPUOnly
    if hasattr(process, "hltIter3IterL3FromL1MuonTrackingRegionsCPUOnly"):
        process.hltIter3IterL3FromL1MuonTrackingRegionsCPUOnly.RegionPSet.input = cms.InputTag( "hltIterL3MuonL1MuonNoL2Selector" )

    process.HLTIterL3muonTkCandidateCPUOnlySequence = cms.Sequence(
        process.HLTDoLocalPixelCPUOnlySequence +
        process.HLTDoLocalStripCPUOnlySequence +
        process.HLTIterL3OIAndIOFromL2muonTkCandidateCPUOnlySequence +
        process.hltL1MuonsPt0 +
        process.hltIterL3MuonL1MuonNoL2Selector + # HERE
        process.HLTIterL3IOmuonFromL1TkCandidateCPUOnlySequence
    )

    return process


### Iter3 in NoVtx
def enableDoubletRecoveryInIOFromL1forNoVtx(process):

    process.hltIter3IterL3FromL1MuonClustersRefRemovalNoVtx = cms.EDProducer( "TrackClusterRemover",
        trajectories = cms.InputTag( "hltIter0IterL3FromL1MuonTrackSelectionHighPurityNoVtx" ),
        trackClassifier = cms.InputTag( '','QualityMasks' ),
        pixelClusters = cms.InputTag( "hltSiPixelClusters" ),
        stripClusters = cms.InputTag( "hltSiStripRawToClustersFacility" ),
        oldClusterRemovalInfo = cms.InputTag( "" ),
        TrackQuality = cms.string( "highPurity" ),
        maxChi2 = cms.double( 16.0 ),
        minNumberOfLayersWithMeasBeforeFiltering = cms.int32( 0 ),
        overrideTrkQuals = cms.InputTag( "" )
    )

    process.hltIter3IterL3FromL1MuonMaskedMeasurementTrackerEventNoVtx = cms.EDProducer( "MaskedMeasurementTrackerEventProducer",
    src = cms.InputTag( "hltMeasurementTrackerEvent" ),
    OnDemand = cms.bool( False ),
    clustersToSkip = cms.InputTag( "hltIter3IterL3FromL1MuonClustersRefRemovalNoVtx" )
    )

    process.hltIter3IterL3FromL1MuonPixelLayersAndRegionsNoVtx = cms.EDProducer( "PixelInactiveAreaTrackingRegionsSeedingLayersProducer",
    RegionPSet = cms.PSet(
      vertexCollection = cms.InputTag( "notUsed" ), # HERE
      beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
      zErrorBeamSpot = cms.double( 24.2 ), # HERE
      extraPhi = cms.double( 0.0 ),
      extraEta = cms.double( 0.0 ),
      maxNVertices = cms.int32( 1 ), # HERE
      nSigmaZVertex = cms.double( 3.0 ),
      nSigmaZBeamSpot = cms.double( 4.0 ),
      ptMin = cms.double( 0.0 ), # HERE
      #operationMode = cms.string( "VerticesFixed" ), # HERE
      searchOpt = cms.bool( False ),
      whereToUseMeasurementTracker = cms.string( "Never" ), # HERE
      originRadius = cms.double( 0.2 ),
      measurementTrackerName = cms.InputTag( "hltIter3IterL3FromL1MuonMaskedMeasurementTrackerEventNoVtx" ),
      precise = cms.bool( True ),
      #zErrorVetex = cms.double( 0.2 ) # HERE
    ),
    inactivePixelDetectorLabels = cms.VInputTag( 'hltSiPixelDigis' ),
    badPixelFEDChannelCollectionLabels = cms.VInputTag( 'hltSiPixelDigis' ),
    ignoreSingleFPixPanelModules = cms.bool( True ),
    debug = cms.untracked.bool( False ),
    createPlottingFiles = cms.untracked.bool( False ),
    layerList = cms.vstring( 'BPix1+BPix2',
      'BPix2+FPix1_pos',
      'BPix2+FPix1_neg',
      'FPix1_pos+FPix2_pos',
      'FPix1_neg+FPix2_neg' ),
    BPix = cms.PSet(
      hitErrorRPhi = cms.double( 0.0027 ),
      TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
      skipClusters = cms.InputTag( "hltIter3IterL3FromL1MuonClustersRefRemovalNoVtx" ),
      useErrorsFromParam = cms.bool( True ),
      hitErrorRZ = cms.double( 0.006 ),
      HitProducer = cms.string( "hltSiPixelRecHits" )
    ),
    FPix = cms.PSet(
      hitErrorRPhi = cms.double( 0.0051 ),
      TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
      skipClusters = cms.InputTag( "hltIter3IterL3FromL1MuonClustersRefRemovalNoVtx" ),
      useErrorsFromParam = cms.bool( True ),
      hitErrorRZ = cms.double( 0.0036 ),
      HitProducer = cms.string( "hltSiPixelRecHits" )
    ),
    TIB = cms.PSet(  ),
    TID = cms.PSet(  ),
    TOB = cms.PSet(  ),
    TEC = cms.PSet(  ),
    MTIB = cms.PSet(  ),
    MTID = cms.PSet(  ),
    MTOB = cms.PSet(  ),
    MTEC = cms.PSet(  )
    )

    process.hltIter3IterL3FromL1MuonTrackingRegionsNoVtx = cms.EDProducer( "L1MuonSeededTrackingRegionsEDProducer",
    CentralBxOnly = cms.bool( True ),
    L1MaxEta = cms.double( 2.5 ),
    L1MinPt = cms.double( 0.0 ),
    L1MinQuality = cms.uint32( 7 ),
    Propagator = cms.string( "SteppingHelixPropagatorAny" ),
    RegionPSet = cms.PSet(
      beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
      deltaEtas = cms.vdouble( 0.175, 0.175, 0.175, 0.175 ), # HERE
      deltaPhis = cms.vdouble( 0.5, 0.4, 0.3, 0.15 ), # HERE
      input = cms.InputTag( "hltIterL3MuonL1MuonNoL2SelectorNoVtx" ),
      maxNRegions = cms.int32( 3 ), # HERE
      maxNVertices = cms.int32( 1 ), # HERE
      measurementTrackerName = cms.InputTag( "hltIter3IterL3FromL1MuonMaskedMeasurementTrackerEventNoVtx" ),
      mode = cms.string( "BeamSpotSigma" ), # HERE
      nSigmaZBeamSpot = cms.double( 4.0 ),
      nSigmaZVertex = cms.double( 3.0 ),
      originRadius = cms.double( 0.2 ), # HERE
      precise = cms.bool( True ),
      ptMin = cms.double( 0.0 ), # HERE
      searchOpt = cms.bool( False ),
      vertexCollection = cms.InputTag( "notUsed" ), # HERE
      whereToUseMeasurementTracker = cms.string( "Never" ), # HERE
      zErrorBeamSpot = cms.double( 24.2 ), # HERE
      zErrorVetex = cms.double( 0.2 ), # HERE
    ),
    ServiceParameters = cms.PSet(
      Propagators = cms.untracked.vstring( [ "SteppingHelixPropagatorAny" ] ),
      RPCLayers = cms.bool( True ),
      UseMuonNavigation = cms.untracked.bool( True ),
    ),
    SetMinPtBarrelTo = cms.double( 3.5 ),
    SetMinPtEndcapTo = cms.double( 1.0 )
    )

    process.hltIter3IterL3FromL1MuonPixelClusterCheckNoVtx = cms.EDProducer( "ClusterCheckerEDProducer",
    doClusterCheck = cms.bool( False ),
    MaxNumberOfStripClusters = cms.uint32( 50000 ),
    ClusterCollectionLabel = cms.InputTag( "hltMeasurementTrackerEvent" ),
    MaxNumberOfPixelClusters = cms.uint32( 40000 ),
    PixelClusterCollectionLabel = cms.InputTag( "hltSiPixelClusters" ),
    cut = cms.string( "" ),
    silentClusterCheck = cms.untracked.bool( False )
    )

    process.hltIter3IterL3FromL1MuonPixelHitDoubletsNoVtx = cms.EDProducer( "HitPairEDProducer",
    seedingLayers = cms.InputTag( "hltIter3IterL3FromL1MuonPixelLayersAndRegionsNoVtx" ),
    trackingRegions = cms.InputTag( "hltIter3IterL3FromL1MuonTrackingRegionsNoVtx" ),
    trackingRegionsSeedingLayers = cms.InputTag( "" ),
    clusterCheck = cms.InputTag( "hltIter3IterL3FromL1MuonPixelClusterCheckNoVtx" ),
    produceSeedingHitSets = cms.bool( True ),
    produceIntermediateHitDoublets = cms.bool( False ),
    maxElement = cms.uint32( 0 ),
    maxElementTotal = cms.uint32( 50000000 ),
    putEmptyIfMaxElementReached = cms.bool( False ),
    layerPairs = cms.vuint32( 0 )
    )

    process.hltIter3IterL3FromL1MuonPixelSeedsNoVtx = cms.EDProducer( "SeedCreatorFromRegionConsecutiveHitsEDProducer",
    seedingHitSets = cms.InputTag( "hltIter3IterL3FromL1MuonPixelHitDoubletsNoVtx" ),
    propagator = cms.string( "PropagatorWithMaterialParabolicMf" ),
    SeedMomentumForBOFF = cms.double( 5.0 ),
    OriginTransverseErrorMultiplier = cms.double( 1.0 ),
    MinOneOverPtError = cms.double( 1.0 ),
    TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
    magneticField = cms.string( "ParabolicMf" ),
    forceKinematicWithRegionDirection = cms.bool( False ),
    SeedComparitorPSet = cms.PSet(  ComponentName = cms.string( "none" ) )
    )

    process.hltIter3IterL3FromL1MuonCkfTrackCandidatesNoVtx = cms.EDProducer( "CkfTrackCandidateMaker",
    cleanTrajectoryAfterInOut = cms.bool( False ),
    doSeedingRegionRebuilding = cms.bool( False ),
    onlyPixelHitsForSeedCleaner = cms.bool( False ),
    reverseTrajectories = cms.bool( False ),
    useHitsSplitting = cms.bool( False ),
    MeasurementTrackerEvent = cms.InputTag( "hltIter3IterL3FromL1MuonMaskedMeasurementTrackerEventNoVtx" ),
    src = cms.InputTag( "hltIter3IterL3FromL1MuonPixelSeedsNoVtx" ),
    clustersToSkip = cms.InputTag( "" ),
    phase2clustersToSkip = cms.InputTag( "" ),
    TrajectoryBuilderPSet = cms.PSet(  refToPSet_ = cms.string( "HLTIter2GroupedCkfTrajectoryBuilderIT" ) ),
    TransientInitialStateEstimatorParameters = cms.PSet(
      propagatorAlongTISE = cms.string( "PropagatorWithMaterialParabolicMf" ),
      numberMeasurementsForFit = cms.int32( 4 ),
      propagatorOppositeTISE = cms.string( "PropagatorWithMaterialParabolicMfOpposite" )
    ),
    numHitsForSeedCleaner = cms.int32( 4 ),
    NavigationSchool = cms.string( "SimpleNavigationSchool" ),
    RedundantSeedCleaner = cms.string( "CachingSeedCleanerBySharedInput" ),
    TrajectoryCleaner = cms.string( "hltESPTrajectoryCleanerBySharedHits" ),
    maxNSeeds = cms.uint32( 100000 ),
    maxSeedsBeforeCleaning = cms.uint32( 1000 )
    )

    process.hltIter3IterL3FromL1MuonCtfWithMaterialTracksNoVtx = cms.EDProducer( "TrackProducer",
    useSimpleMF = cms.bool( True ),
    SimpleMagneticField = cms.string( "ParabolicMf" ),
    src = cms.InputTag( "hltIter3IterL3FromL1MuonCkfTrackCandidatesNoVtx" ),
    clusterRemovalInfo = cms.InputTag( "" ),
    beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
    Fitter = cms.string( "hltESPFittingSmootherIT" ),
    useHitsSplitting = cms.bool( False ),
    alias = cms.untracked.string( "ctfWithMaterialTracks" ),
    TrajectoryInEvent = cms.bool( False ),
    TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
    AlgorithmName = cms.string( "hltIter3IterL3FromL1Muon" ),
    Propagator = cms.string( "hltESPRungeKuttaTrackerPropagator" ),
    GeometricInnerState = cms.bool( True ),
    NavigationSchool = cms.string( "" ),
    MeasurementTracker = cms.string( "" ),
    MeasurementTrackerEvent = cms.InputTag( "hltIter3IterL3FromL1MuonMaskedMeasurementTrackerEventNoVtx" )
    )

    process.hltIter3IterL3FromL1MuonTrackCutClassifierNoVtx = cms.EDProducer( "TrackCutClassifier",
    src = cms.InputTag( "hltIter3IterL3FromL1MuonCtfWithMaterialTracksNoVtx" ),
    beamspot = cms.InputTag( "hltOnlineBeamSpot" ),
    vertices = cms.InputTag( "hltTrimmedPixelVertices" ),
    ignoreVertices = cms.bool( False ),
    qualityCuts = cms.vdouble( -0.7, 0.1, 0.7 ),
    mva = cms.PSet(
      minPixelHits = cms.vint32( 0, 0, 0 ),
      maxDzWrtBS = cms.vdouble( 3.40282346639e+38, 24, 100 ), # HERE
      dr_par = cms.PSet(
        d0err = cms.vdouble( 0.003, 0.003, 3.40282346639e+38 ), # HERE
        d0err_par = cms.vdouble( 0.001, 0.001, 3.40282346639e+38 ), # HERE
        dr_exp = cms.vint32( 4, 4, 2147483647 ), # HERE
        dr_par1 = cms.vdouble( 0.4, 0.4, 3.40282346639e+38 ), # HERE
        dr_par2 = cms.vdouble( 0.3, 0.3, 3.40282346639e+38 ), # HERE
      ),
      maxLostLayers = cms.vint32( 1, 1, 1 ),
      min3DLayers = cms.vint32( 0, 0, 0 ),
      dz_par = cms.PSet(
        dz_exp = cms.vint32( 4, 4, 2147483647 ), # HERE
        dz_par1 = cms.vdouble( 0.4, 0.4, 3.40282346639e+38 ), # HERE
        dz_par2 = cms.vdouble( 0.35, 0.35, 3.40282346639e+38 ), # HERE
      ),
      minNVtxTrk = cms.int32( 3 ),
      maxChi2 = cms.vdouble( 3.40282346639e+38, 3.40282346639e+38, 3.40282346639e+38 ), # HERE
      maxChi2n = cms.vdouble( 1.2, 1, 0.7 ), # HERE
      minNdof = cms.vdouble( 1.0E-5, 1.0E-5, 1.0E-5 ),
      maxDr = cms.vdouble( 0.5, 0.03, 3.40282346639E38 ),
      maxDz = cms.vdouble( 0.5, 0.2, 3.40282346639e+38 ), # HERE
      minLayers = cms.vint32( 3, 3, 4 ) # HERE
    )
    )

    process.hltIter3IterL3FromL1MuonTrackSelectionHighPurityNoVtx = cms.EDProducer( "TrackCollectionFilterCloner",
    originalSource = cms.InputTag( "hltIter3IterL3FromL1MuonCtfWithMaterialTracksNoVtx" ),
    originalMVAVals = cms.InputTag( 'hltIter3IterL3FromL1MuonTrackCutClassifierNoVtx','MVAValues' ),
    originalQualVals = cms.InputTag( 'hltIter3IterL3FromL1MuonTrackCutClassifierNoVtx','QualityMasks' ),
    minQuality = cms.string( "highPurity" ),
    copyExtras = cms.untracked.bool( True ),
    copyTrajectories = cms.untracked.bool( False )
    )

    process.hltIter03IterL3FromL1MuonMergedNoVtx  = cms.EDProducer( "TrackListMerger",
        ShareFrac = cms.double( 0.19 ),
        FoundHitBonus = cms.double( 5.0 ),
        LostHitPenalty = cms.double( 20.0 ),
        MinPT = cms.double( 0.05 ),
        Epsilon = cms.double( -0.001 ),
        MaxNormalizedChisq = cms.double( 1000.0 ),
        MinFound = cms.int32( 3 ),
        TrackProducers = cms.VInputTag( 'hltIter0IterL3FromL1MuonTrackSelectionHighPurityNoVtx','hltIter3IterL3FromL1MuonTrackSelectionHighPurityNoVtx' ),
        hasSelector = cms.vint32( 0, 0 ),
        indivShareFrac = cms.vdouble( 1.0, 1.0 ),
        selectedTrackQuals = cms.VInputTag( 'hltIter0IterL3FromL1MuonTrackSelectionHighPurityNoVtx','hltIter3IterL3FromL1MuonTrackSelectionHighPurityNoVtx' ),
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

    process.hltIterL3MuonAndMuonFromL1MergedNoVtx.TrackProducers = cms.VInputTag( 'hltIterL3MuonMergedNoVtx','hltIter03IterL3FromL1MuonMergedNoVtx' )
    process.hltIterL3MuonAndMuonFromL1MergedNoVtx.selectedTrackQuals = cms.VInputTag( 'hltIterL3MuonMergedNoVtx','hltIter03IterL3FromL1MuonMergedNoVtx' )

    process.HLTIterativeTrackingIteration3ForIterL3FromL1MuonNoVtx = cms.Sequence(
        process.hltIter3IterL3FromL1MuonClustersRefRemovalNoVtx +
        process.hltIter3IterL3FromL1MuonMaskedMeasurementTrackerEventNoVtx +
        process.hltIter3IterL3FromL1MuonPixelLayersAndRegionsNoVtx +
        process.hltIter3IterL3FromL1MuonTrackingRegionsNoVtx +
        process.hltIter3IterL3FromL1MuonPixelClusterCheckNoVtx +
        process.hltIter3IterL3FromL1MuonPixelHitDoubletsNoVtx +
        process.hltIter3IterL3FromL1MuonPixelSeedsNoVtx +
        process.hltIter3IterL3FromL1MuonCkfTrackCandidatesNoVtx +
        process.hltIter3IterL3FromL1MuonCtfWithMaterialTracksNoVtx +
        process.hltIter3IterL3FromL1MuonTrackCutClassifierNoVtx +
        process.hltIter3IterL3FromL1MuonTrackSelectionHighPurityNoVtx
    )

    process.HLTIterL3IOmuonFromL1TkCandidateSequenceNoVtx = cms.Sequence(
        process.HLTRecopixelvertexingSequenceForIterL3FromL1MuonNoVtx +
        process.HLTIterativeTrackingIteration0ForIterL3FromL1MuonNoVtx +
        process.HLTIterativeTrackingIteration3ForIterL3FromL1MuonNoVtx
    )

    process.HLTL3muonrecoNocandSequenceNoVtx = cms.Sequence(
        process.HLTIterL3muonTkCandidateSequenceNoVtx +
        process.hltIter03IterL3FromL1MuonMergedNoVtx +
        process.hltIterL3MuonMergedNoVtx +
        process.hltIterL3MuonAndMuonFromL1MergedNoVtx +
        process.hltL3MuonsIterL3LinksNoVtx +
        process.hltIterL3MuonsNoVtx
    )

    return process

### Iter3 with CPUOnly
def enableDoubletRecoveryInIOFromL1CPUOnly(process):

    process.hltIter3IterL3FromL1MuonClustersRefRemovalCPUOnly = cms.EDProducer( "TrackClusterRemover",
        trajectories = cms.InputTag( "hltIter0IterL3FromL1MuonTrackSelectionHighPurityCPUOnly" ),
        trackClassifier = cms.InputTag( '','QualityMasks' ),
        pixelClusters = cms.InputTag( "hltSiPixelClustersLegacy" ),
        stripClusters = cms.InputTag( "hltSiStripRawToClustersFacility" ),
        oldClusterRemovalInfo = cms.InputTag( "" ),
        TrackQuality = cms.string( "highPurity" ),
        maxChi2 = cms.double( 16.0 ),
        minNumberOfLayersWithMeasBeforeFiltering = cms.int32( 0 ),
        overrideTrkQuals = cms.InputTag( "" )
    )

    process.hltIter3IterL3FromL1MuonMaskedMeasurementTrackerEventCPUOnly = cms.EDProducer( "MaskedMeasurementTrackerEventProducer",
    src = cms.InputTag( "hltMeasurementTrackerEventCPUOnly" ),
    OnDemand = cms.bool( False ),
    clustersToSkip = cms.InputTag( "hltIter3IterL3FromL1MuonClustersRefRemovalCPUOnly" )
    )

    process.hltIter3IterL3FromL1MuonPixelLayersAndRegionsCPUOnly = cms.EDProducer( "PixelInactiveAreaTrackingRegionsSeedingLayersProducer",
    RegionPSet = cms.PSet(
      vertexCollection = cms.InputTag( "hltTrimmedPixelVerticesCPUOnly" ),
      beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
      zErrorBeamSpot = cms.double( 15.0 ),
      extraPhi = cms.double( 0.0 ),
      extraEta = cms.double( 0.0 ),
      maxNVertices = cms.int32( 3 ),
      nSigmaZVertex = cms.double( 3.0 ),
      nSigmaZBeamSpot = cms.double( 4.0 ),
      ptMin = cms.double( 1.2 ),
      operationMode = cms.string( "VerticesFixed" ),
      searchOpt = cms.bool( False ),
      whereToUseMeasurementTracker = cms.string( "ForSiStrips" ),
      originRadius = cms.double( 0.015 ),
      measurementTrackerName = cms.InputTag( "hltIter3IterL3FromL1MuonMaskedMeasurementTrackerEventCPUOnly" ),
      precise = cms.bool( True ),
      zErrorVertex = cms.double( 0.03 )
    ),
    inactivePixelDetectorLabels = cms.VInputTag( 'hltSiPixelDigisLegacy' ),
    badPixelFEDChannelCollectionLabels = cms.VInputTag( 'hltSiPixelDigisLegacy' ),
    ignoreSingleFPixPanelModules = cms.bool( True ),
    debug = cms.untracked.bool( False ),
    createPlottingFiles = cms.untracked.bool( False ),
    layerList = cms.vstring( 'BPix1+BPix2',
      'BPix2+FPix1_pos',
      'BPix2+FPix1_neg',
      'FPix1_pos+FPix2_pos',
      'FPix1_neg+FPix2_neg' ),
    BPix = cms.PSet(
      hitErrorRPhi = cms.double( 0.0027 ),
      TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
      skipClusters = cms.InputTag( "hltIter3IterL3FromL1MuonClustersRefRemovalCPUOnly" ),
      useErrorsFromParam = cms.bool( True ),
      hitErrorRZ = cms.double( 0.006 ),
      HitProducer = cms.string( "hltSiPixelRecHitsFromLegacyCPUOnly" )
    ),
    FPix = cms.PSet(
      hitErrorRPhi = cms.double( 0.0051 ),
      TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
      skipClusters = cms.InputTag( "hltIter3IterL3FromL1MuonClustersRefRemovalCPUOnly" ),
      useErrorsFromParam = cms.bool( True ),
      hitErrorRZ = cms.double( 0.0036 ),
      HitProducer = cms.string( "hltSiPixelRecHitsFromLegacyCPUOnly" )
    ),
    TIB = cms.PSet(  ),
    TID = cms.PSet(  ),
    TOB = cms.PSet(  ),
    TEC = cms.PSet(  ),
    MTIB = cms.PSet(  ),
    MTID = cms.PSet(  ),
    MTOB = cms.PSet(  ),
    MTEC = cms.PSet(  )
    )

    process.hltIter3IterL3FromL1MuonTrackingRegionsCPUOnly = cms.EDProducer( "L1MuonSeededTrackingRegionsEDProducer",
    Propagator = cms.string( "SteppingHelixPropagatorAny" ),
    L1MinPt = cms.double( 0.0 ),
    L1MaxEta = cms.double( 2.5 ),
    L1MinQuality = cms.uint32( 7 ),
    SetMinPtBarrelTo = cms.double( 3.5 ),
    SetMinPtEndcapTo = cms.double( 1.0 ),
    CentralBxOnly = cms.bool( True ),
    RegionPSet = cms.PSet(
      vertexCollection = cms.InputTag( "hltTrimmedPixelVerticesCPUOnly" ),
      deltaEtas = cms.vdouble( 0.175, 0.175, 0.175, 0.175 ),
      beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
      zErrorBeamSpot = cms.double( 15.0 ),
      maxNVertices = cms.int32( 3 ),
      maxNRegions = cms.int32( 3 ),
      nSigmaZVertex = cms.double( 3.0 ),
      nSigmaZBeamSpot = cms.double( 4.0 ),
      ptMin = cms.double( 1.2 ),
      mode = cms.string( "VerticesFixed" ),
      input = cms.InputTag( "hltL1MuonsPt0" ),
      ptRanges = cms.vdouble( 0.0, 10.0, 15.0, 20.0, 1.0E64 ),
      searchOpt = cms.bool( False ),
      deltaPhis = cms.vdouble( 0.5, 0.4, 0.3, 0.15 ),
      whereToUseMeasurementTracker = cms.string( "ForSiStrips" ),
      originRadius = cms.double( 0.015 ),
      measurementTrackerName = cms.InputTag( "hltIter3IterL3FromL1MuonMaskedMeasurementTrackerEventCPUOnly" ),
      precise = cms.bool( True )
    ),
    ServiceParameters = cms.PSet(
      RPCLayers = cms.bool( True ),
      UseMuonNavigation = cms.untracked.bool( True ),
      Propagators = cms.untracked.vstring( 'SteppingHelixPropagatorAny' )
    )
    )

    process.hltIter3IterL3FromL1MuonPixelClusterCheckCPUOnly = cms.EDProducer( "ClusterCheckerEDProducer",
    doClusterCheck = cms.bool( False ),
    MaxNumberOfStripClusters = cms.uint32( 50000 ),
    ClusterCollectionLabel = cms.InputTag( "hltMeasurementTrackerEventCPUOnly" ),
    MaxNumberOfPixelClusters = cms.uint32( 40000 ),
    PixelClusterCollectionLabel = cms.InputTag( "hltSiPixelClustersLegacy" ),
    cut = cms.string( "" ),
    silentClusterCheck = cms.untracked.bool( False )
    )

    process.hltIter3IterL3FromL1MuonPixelHitDoubletsCPUOnly = cms.EDProducer( "HitPairEDProducer",
    seedingLayers = cms.InputTag( "hltIter3IterL3FromL1MuonPixelLayersAndRegionsCPUOnly" ),
    trackingRegions = cms.InputTag( "hltIter3IterL3FromL1MuonTrackingRegionsCPUOnly" ),
    trackingRegionsSeedingLayers = cms.InputTag( "" ),
    clusterCheck = cms.InputTag( "hltIter3IterL3FromL1MuonPixelClusterCheckCPUOnly" ),
    produceSeedingHitSets = cms.bool( True ),
    produceIntermediateHitDoublets = cms.bool( False ),
    maxElement = cms.uint32( 0 ),
    maxElementTotal = cms.uint32( 50000000 ),
    putEmptyIfMaxElementReached = cms.bool( False ),
    layerPairs = cms.vuint32( 0 )
    )

    process.hltIter3IterL3FromL1MuonPixelSeedsCPUOnly = cms.EDProducer( "SeedCreatorFromRegionConsecutiveHitsEDProducer",
    seedingHitSets = cms.InputTag( "hltIter3IterL3FromL1MuonPixelHitDoubletsCPUOnly" ),
    propagator = cms.string( "PropagatorWithMaterialParabolicMf" ),
    SeedMomentumForBOFF = cms.double( 5.0 ),
    OriginTransverseErrorMultiplier = cms.double( 1.0 ),
    MinOneOverPtError = cms.double( 1.0 ),
    TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
    magneticField = cms.string( "ParabolicMf" ),
    forceKinematicWithRegionDirection = cms.bool( False ),
    SeedComparitorPSet = cms.PSet(  ComponentName = cms.string( "none" ) )
    )

    process.hltIter3IterL3FromL1MuonCkfTrackCandidatesCPUOnly = cms.EDProducer( "CkfTrackCandidateMaker",
    cleanTrajectoryAfterInOut = cms.bool( False ),
    doSeedingRegionRebuilding = cms.bool( False ),
    onlyPixelHitsForSeedCleaner = cms.bool( False ),
    reverseTrajectories = cms.bool( False ),
    useHitsSplitting = cms.bool( False ),
    MeasurementTrackerEvent = cms.InputTag( "hltIter3IterL3FromL1MuonMaskedMeasurementTrackerEventCPUOnly" ),
    src = cms.InputTag( "hltIter3IterL3FromL1MuonPixelSeedsCPUOnly" ),
    clustersToSkip = cms.InputTag( "" ),
    phase2clustersToSkip = cms.InputTag( "" ),
    TrajectoryBuilderPSet = cms.PSet(  refToPSet_ = cms.string( "HLTIter2GroupedCkfTrajectoryBuilderIT" ) ),
    TransientInitialStateEstimatorParameters = cms.PSet(
      propagatorAlongTISE = cms.string( "PropagatorWithMaterialParabolicMf" ),
      numberMeasurementsForFit = cms.int32( 4 ),
      propagatorOppositeTISE = cms.string( "PropagatorWithMaterialParabolicMfOpposite" )
    ),
    numHitsForSeedCleaner = cms.int32( 4 ),
    NavigationSchool = cms.string( "SimpleNavigationSchool" ),
    RedundantSeedCleaner = cms.string( "CachingSeedCleanerBySharedInput" ),
    TrajectoryCleaner = cms.string( "hltESPTrajectoryCleanerBySharedHits" ),
    maxNSeeds = cms.uint32( 100000 ),
    maxSeedsBeforeCleaning = cms.uint32( 1000 )
    )

    process.hltIter3IterL3FromL1MuonCtfWithMaterialTracksCPUOnly = cms.EDProducer( "TrackProducer",
    useSimpleMF = cms.bool( True ),
    SimpleMagneticField = cms.string( "ParabolicMf" ),
    src = cms.InputTag( "hltIter3IterL3FromL1MuonCkfTrackCandidatesCPUOnly" ),
    clusterRemovalInfo = cms.InputTag( "" ),
    beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
    Fitter = cms.string( "hltESPFittingSmootherIT" ),
    useHitsSplitting = cms.bool( False ),
    alias = cms.untracked.string( "ctfWithMaterialTracks" ),
    TrajectoryInEvent = cms.bool( False ),
    TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
    AlgorithmName = cms.string( "hltIter3IterL3FromL1Muon" ),
    Propagator = cms.string( "hltESPRungeKuttaTrackerPropagator" ),
    GeometricInnerState = cms.bool( True ),
    NavigationSchool = cms.string( "" ),
    MeasurementTracker = cms.string( "" ),
    MeasurementTrackerEvent = cms.InputTag( "hltIter3IterL3FromL1MuonMaskedMeasurementTrackerEventCPUOnly" )
    )

    process.hltIter3IterL3FromL1MuonTrackCutClassifierCPUOnly = cms.EDProducer( "TrackCutClassifier",
    src = cms.InputTag( "hltIter3IterL3FromL1MuonCtfWithMaterialTracksCPUOnly" ),
    beamspot = cms.InputTag( "hltOnlineBeamSpot" ),
    vertices = cms.InputTag( "hltTrimmedPixelVerticesCPUOnly" ),
    ignoreVertices = cms.bool( False ),
    qualityCuts = cms.vdouble( -0.7, 0.1, 0.7 ),
    mva = cms.PSet(
      minPixelHits = cms.vint32( 0, 0, 0 ),
      maxDzWrtBS = cms.vdouble( 3.40282346639E38, 24.0, 15.0 ),
      dr_par = cms.PSet(
        d0err = cms.vdouble( 0.003, 0.003, 0.003 ),
        dr_par2 = cms.vdouble( 3.40282346639E38, 0.3, 0.3 ),
        dr_par1 = cms.vdouble( 3.40282346639E38, 0.4, 0.4 ),
        dr_exp = cms.vint32( 4, 4, 4 ),
        d0err_par = cms.vdouble( 0.001, 0.001, 0.001 )
      ),
      maxLostLayers = cms.vint32( 1, 1, 1 ),
      min3DLayers = cms.vint32( 0, 0, 0 ),
      dz_par = cms.PSet(
        dz_par1 = cms.vdouble( 3.40282346639E38, 0.4, 0.4 ),
        dz_par2 = cms.vdouble( 3.40282346639E38, 0.35, 0.35 ),
        dz_exp = cms.vint32( 4, 4, 4 )
      ),
      minNVtxTrk = cms.int32( 3 ),
      maxDz = cms.vdouble( 0.5, 0.2, 3.40282346639E38 ),
      minNdof = cms.vdouble( 1.0E-5, 1.0E-5, 1.0E-5 ),
      maxChi2 = cms.vdouble( 9999.0, 25.0, 16.0 ),
      maxChi2n = cms.vdouble( 1.2, 1.0, 0.7 ),
      maxDr = cms.vdouble( 0.5, 0.03, 3.40282346639E38 ),
      minLayers = cms.vint32( 3, 3, 3 )
    )
    )

    process.hltIter3IterL3FromL1MuonTrackSelectionHighPurityCPUOnly = cms.EDProducer( "TrackCollectionFilterCloner",
    originalSource = cms.InputTag( "hltIter3IterL3FromL1MuonCtfWithMaterialTracksCPUOnly" ),
    originalMVAVals = cms.InputTag( 'hltIter3IterL3FromL1MuonTrackCutClassifierCPUOnly','MVAValues' ),
    originalQualVals = cms.InputTag( 'hltIter3IterL3FromL1MuonTrackCutClassifierCPUOnly','QualityMasks' ),
    minQuality = cms.string( "highPurity" ),
    copyExtras = cms.untracked.bool( True ),
    copyTrajectories = cms.untracked.bool( False )
    )

    process.hltIter03IterL3FromL1MuonMergedCPUOnly  = cms.EDProducer( "TrackListMerger",
        ShareFrac = cms.double( 0.19 ),
        FoundHitBonus = cms.double( 5.0 ),
        LostHitPenalty = cms.double( 20.0 ),
        MinPT = cms.double( 0.05 ),
        Epsilon = cms.double( -0.001 ),
        MaxNormalizedChisq = cms.double( 1000.0 ),
        MinFound = cms.int32( 3 ),
        TrackProducers = cms.VInputTag( 'hltIter0IterL3FromL1MuonTrackSelectionHighPurityCPUOnly','hltIter3IterL3FromL1MuonTrackSelectionHighPurityCPUOnly' ),
        hasSelector = cms.vint32( 0, 0 ),
        indivShareFrac = cms.vdouble( 1.0, 1.0 ),
        selectedTrackQuals = cms.VInputTag( 'hltIter0IterL3FromL1MuonTrackSelectionHighPurityCPUOnly','hltIter3IterL3FromL1MuonTrackSelectionHighPurityCPUOnly' ),
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

    process.hltIterL3MuonAndMuonFromL1MergedCPUOnly.TrackProducers = cms.VInputTag( 'hltIterL3MuonMergedCPUOnly','hltIter03IterL3FromL1MuonMergedCPUOnly' )
    process.hltIterL3MuonAndMuonFromL1MergedCPUOnly.selectedTrackQuals = cms.VInputTag( 'hltIterL3MuonMergedCPUOnly','hltIter03IterL3FromL1MuonMergedCPUOnly' )
    process.hltIterL3MuonsNoIDCPUOnly.TrackExtractorPSet.inputTrackCollection = cms.InputTag( "hltIter03IterL3FromL1MuonMergedCPUOnly" )

    process.HLTIterativeTrackingIteration3ForIterL3FromL1MuonCPUOnly = cms.Sequence(
        process.hltIter3IterL3FromL1MuonClustersRefRemovalCPUOnly +
        process.hltIter3IterL3FromL1MuonMaskedMeasurementTrackerEventCPUOnly +
        process.hltIter3IterL3FromL1MuonPixelLayersAndRegionsCPUOnly +
        process.hltIter3IterL3FromL1MuonTrackingRegionsCPUOnly +
        process.hltIter3IterL3FromL1MuonPixelClusterCheckCPUOnly +
        process.hltIter3IterL3FromL1MuonPixelHitDoubletsCPUOnly +
        process.hltIter3IterL3FromL1MuonPixelSeedsCPUOnly +
        process.hltIter3IterL3FromL1MuonCkfTrackCandidatesCPUOnly +
        process.hltIter3IterL3FromL1MuonCtfWithMaterialTracksCPUOnly +
        process.hltIter3IterL3FromL1MuonTrackCutClassifierCPUOnly +
        process.hltIter3IterL3FromL1MuonTrackSelectionHighPurityCPUOnly
    )

    process.HLTIterL3IOmuonFromL1TkCandidateCPUOnlySequence = cms.Sequence(
        process.HLTRecopixelvertexingCPUOnlySequenceForIterL3FromL1Muon +
        process.HLTIterativeTrackingIteration0ForIterL3FromL1MuonCPUOnly +
        process.HLTIterativeTrackingIteration3ForIterL3FromL1MuonCPUOnly
    )

    process.HLTL3muonrecoNocandCPUOnlySequence = cms.Sequence(
        process.HLTIterL3muonTkCandidateCPUOnlySequence +
        process.hltIter03IterL3FromL1MuonMergedCPUOnly +
        process.hltIterL3MuonMergedCPUOnly +
        process.hltIterL3MuonAndMuonFromL1MergedCPUOnly +
        process.hltIterL3GlbMuonCPUOnly +
        process.hltIterL3MuonsNoIDCPUOnly +
        process.hltIterL3MuonsCPUOnly +
        process.hltL3MuonsIterL3LinksCPUOnly +
        process.hltIterL3MuonTracksCPUOnly
    )

    return process


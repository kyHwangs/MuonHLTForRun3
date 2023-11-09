import FWCore.ParameterSet.Config as cms

from HLTrigger.Configuration.common import *


def enableDoubletRecoveryInIOFromL2(process):

    # IO FROM L2

    process.hltIter3IterL3MuonClustersRefRemoval = cms.EDProducer( "TrackClusterRemover",
        trajectories = cms.InputTag( "hltIter0IterL3MuonTrackSelectionHighPurity" ), ## HERE
        trackClassifier = cms.InputTag( '','QualityMasks' ),
        pixelClusters = cms.InputTag( "hltSiPixelClusters" ),
        stripClusters = cms.InputTag( "hltSiStripRawToClustersFacility" ),
        oldClusterRemovalInfo = cms.InputTag( "" ),
        TrackQuality = cms.string( "highPurity" ),
        maxChi2 = cms.double( 16.0 ),
        minNumberOfLayersWithMeasBeforeFiltering = cms.int32( 0 ),
        overrideTrkQuals = cms.InputTag( "" )
    )

    process.hltIter3IterL3MuonMaskedMeasurementTrackerEvent = cms.EDProducer( "MaskedMeasurementTrackerEventProducer",
    src = cms.InputTag( "hltMeasurementTrackerEvent" ),
    OnDemand = cms.bool( False ),
    clustersToSkip = cms.InputTag( "hltIter3IterL3MuonClustersRefRemoval" )
    )

    process.hltIter3IterL3MuonPixelLayersAndRegions = cms.EDProducer( "PixelInactiveAreaTrackingRegionsSeedingLayersProducer",
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
      measurementTrackerName = cms.InputTag( "hltIter3IterL3MuonMaskedMeasurementTrackerEvent" ),
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
      skipClusters = cms.InputTag( "hltIter3IterL3MuonClustersRefRemoval" ),
      useErrorsFromParam = cms.bool( True ),
      hitErrorRZ = cms.double( 0.006 ),
      HitProducer = cms.string( "hltSiPixelRecHits" )
    ),
    FPix = cms.PSet(
      hitErrorRPhi = cms.double( 0.0051 ),
      TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
      skipClusters = cms.InputTag( "hltIter3IterL3MuonClustersRefRemoval" ),
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


    ## pt-dep ROI - from Run3 (hltIterL3MuonPixelTracksTrackingRegions)
    process.hltIter3IterL3MuonTrackingRegions = cms.EDProducer( "MuonTrackingRegionByPtEDProducer",
        DeltaR = cms.double( 0.025 ),
        beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
        OnDemand = cms.int32( -1 ),
        vertexCollection = cms.InputTag( "hltTrimmedPixelVertices" ), # HERE
        MeasurementTrackerName = cms.InputTag( "hltIter2IterL3MuonMaskedMeasurementTrackerEvent" ), # HERE
        UseVertex = cms.bool( False ),
        Rescale_Dz = cms.double( 4.0 ),
        Pt_fixed = cms.bool( True ),
        Z_fixed = cms.bool( True ),
        Pt_min = cms.double( 1.2 ), # HERE
        DeltaZ = cms.double( 15.0 ), # HERE
        ptRanges = cms.vdouble( 0.0, 15.0, 20.0, 1.0E64 ),
        deltaEtas = cms.vdouble( 0.2, 0.2, 0.2 ),
        deltaPhis = cms.vdouble( 0.75, 0.45, 0.225 ),
        maxRegions = cms.int32( 5 ),
        precise = cms.bool( True ),
        input = cms.InputTag( "hltL2SelectorForL3IO" )
        )

    process.hltIter3IterL3MuonPixelClusterCheck = cms.EDProducer( "ClusterCheckerEDProducer",
    doClusterCheck = cms.bool( False ),
    MaxNumberOfCosmicClusters = cms.uint32( 50000 ),
    ClusterCollectionLabel = cms.InputTag( "hltMeasurementTrackerEvent" ),
    MaxNumberOfPixelClusters = cms.uint32( 40000 ),
    PixelClusterCollectionLabel = cms.InputTag( "hltSiPixelClusters" ),
    cut = cms.string( "" ),
    silentClusterCheck = cms.untracked.bool( False )
    )

    process.hltIter3IterL3MuonPixelHitDoublets = cms.EDProducer( "HitPairEDProducer",
    seedingLayers = cms.InputTag( "hltIter3IterL3MuonPixelLayersAndRegions" ), ## HERE
    trackingRegions = cms.InputTag( "hltIter3IterL3MuonTrackingRegions" ), ## HERE
    trackingRegionsSeedingLayers = cms.InputTag( "" ), ## HERE
    clusterCheck = cms.InputTag( "hltIter3IterL3MuonPixelClusterCheck" ),
    produceSeedingHitSets = cms.bool( True ),
    produceIntermediateHitDoublets = cms.bool( False ),
    maxElement = cms.uint32( 0 ),
    maxElementTotal = cms.uint32( 50000000 ),
    putEmptyIfMaxElementReached = cms.bool( False ),
    layerPairs = cms.vuint32( 0 )
    )

    process.hltIter3IterL3MuonPixelSeeds = cms.EDProducer( "SeedCreatorFromRegionConsecutiveHitsEDProducer",
    seedingHitSets = cms.InputTag( "hltIter3IterL3MuonPixelHitDoublets" ),
    propagator = cms.string( "PropagatorWithMaterialParabolicMf" ),
    SeedMomentumForBOFF = cms.double( 5.0 ),
    OriginTransverseErrorMultiplier = cms.double( 1.0 ),
    MinOneOverPtError = cms.double( 1.0 ),
    TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
    magneticField = cms.string( "ParabolicMf" ),
    forceKinematicWithRegionDirection = cms.bool( False ),
    SeedComparitorPSet = cms.PSet(  ComponentName = cms.string( "none" ) )
    )

    process.hltIter3IterL3MuonCkfTrackCandidates = cms.EDProducer( "CkfTrackCandidateMaker",
    cleanTrajectoryAfterInOut = cms.bool( False ),
    doSeedingRegionRebuilding = cms.bool( False ),
    onlyPixelHitsForSeedCleaner = cms.bool( False ),
    reverseTrajectories = cms.bool( False ),
    useHitsSplitting = cms.bool( False ),
    MeasurementTrackerEvent = cms.InputTag( "hltIter3IterL3MuonMaskedMeasurementTrackerEvent" ),
    src = cms.InputTag( "hltIter3IterL3MuonPixelSeeds" ),
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

    process.hltIter3IterL3MuonCtfWithMaterialTracks = cms.EDProducer( "TrackProducer",
    useSimpleMF = cms.bool( True ),
    SimpleMagneticField = cms.string( "ParabolicMf" ),
    src = cms.InputTag( "hltIter3IterL3MuonCkfTrackCandidates" ),
    clusterRemovalInfo = cms.InputTag( "" ),
    beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
    Fitter = cms.string( "hltESPFittingSmootherIT" ),
    useHitsSplitting = cms.bool( False ),
    alias = cms.untracked.string( "ctfWithMaterialTracks" ),
    TrajectoryInEvent = cms.bool( False ),
    TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
    AlgorithmName = cms.string( "hltIter3IterL3Muon" ),
    Propagator = cms.string( "hltESPRungeKuttaTrackerPropagator" ),
    GeometricInnerState = cms.bool( True ),
    NavigationSchool = cms.string( "" ),
    MeasurementTracker = cms.string( "" ),
    MeasurementTrackerEvent = cms.InputTag( "hltIter3IterL3MuonMaskedMeasurementTrackerEvent" )
    )

    process.hltIter3IterL3MuonTrackCutClassifier = cms.EDProducer( "TrackCutClassifier",
    src = cms.InputTag( "hltIter3IterL3MuonCtfWithMaterialTracks" ),
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

    process.hltIter3IterL3MuonTrackSelectionHighPurity = cms.EDProducer( "TrackCollectionFilterCloner",
    originalSource = cms.InputTag( "hltIter3IterL3MuonCtfWithMaterialTracks" ),
    originalMVAVals = cms.InputTag( 'hltIter3IterL3MuonTrackCutClassifier','MVAValues' ),
    originalQualVals = cms.InputTag( 'hltIter3IterL3MuonTrackCutClassifier','QualityMasks' ),
    minQuality = cms.string( "highPurity" ),
    copyExtras = cms.untracked.bool( True ),
    copyTrajectories = cms.untracked.bool( False )
    )

    ## New track merger
    process.hltIter03IterL3MuonMerged  = cms.EDProducer( "TrackListMerger",
        ShareFrac = cms.double( 0.19 ),
        FoundHitBonus = cms.double( 5.0 ),
        LostHitPenalty = cms.double( 20.0 ),
        MinPT = cms.double( 0.05 ),
        Epsilon = cms.double( -0.001 ),
        MaxNormalizedChisq = cms.double( 1000.0 ),
        MinFound = cms.int32( 3 ),
        TrackProducers = cms.VInputTag( 'hltIter0IterL3MuonTrackSelectionHighPurity','hltIter3IterL3MuonTrackSelectionHighPurity' ),
        hasSelector = cms.vint32( 0, 0 ),
        indivShareFrac = cms.vdouble( 1.0, 1.0 ),
        selectedTrackQuals = cms.VInputTag( 'hltIter0IterL3MuonTrackSelectionHighPurity','hltIter3IterL3MuonTrackSelectionHighPurity' ),
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

    process.hltIterL3MuonMerged.TrackProducers = cms.VInputTag( 'hltIterL3OIMuonTrackSelectionHighPurity','hltIter03IterL3MuonMerged' )
    process.hltIterL3MuonMerged.selectedTrackQuals = cms.VInputTag( 'hltIterL3OIMuonTrackSelectionHighPurity','hltIter03IterL3MuonMerged' )
    process.hltL3MuonsIterL3IO.L3TrajBuilderParameters.tkTrajLabel = cms.InputTag( "hltIter03IterL3MuonMerged" )

    process.HLTIterativeTrackingIteration3ForIterL3Muon = cms.Sequence(
        process.hltIter3IterL3MuonClustersRefRemoval +
        process.hltIter3IterL3MuonMaskedMeasurementTrackerEvent +
        process.hltIter3IterL3MuonPixelLayersAndRegions +
        process.hltIter3IterL3MuonTrackingRegions + # HERE
        process.hltIter3IterL3MuonPixelClusterCheck +
        process.hltIter3IterL3MuonPixelHitDoublets +
        process.hltIter3IterL3MuonPixelSeeds +
        process.hltIter3IterL3MuonCkfTrackCandidates +
        process.hltIter3IterL3MuonCtfWithMaterialTracks +
        process.hltIter3IterL3MuonTrackCutClassifier +
        process.hltIter3IterL3MuonTrackSelectionHighPurity
    )

    process.HLTIterL3IOmuonTkCandidateSequence = cms.Sequence(
        process.HLTIterL3MuonRecopixelvertexingSequence +
        process.HLTIterativeTrackingIteration0ForIterL3Muon +
        process.HLTIterativeTrackingIteration3ForIterL3Muon + ## HERE
        process.hltIter03IterL3MuonMerged + ## HERE
        process.hltL3MuonsIterL3IO
    )

    return process


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

    '''## fixed ROI - from Run2 (hltIter3IterL3FromL1MuonTrackingRegions)
    process.hltIter3IterL3FromL1MuonTrackingRegions = cms.EDProducer( "CandidateSeededTrackingRegionsEDProducer",
    RegionPSet = cms.PSet(
      vertexCollection = cms.InputTag( "hltTrimmedPixelVertices" ),
      beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
      zErrorBeamSpot = cms.double( 15.0 ),
      maxNVertices = cms.int32( 3 ),
      nSigmaZVertex = cms.double( 3.0 ),
      nSigmaZBeamSpot = cms.double( 4.0 ),
      ptMin = cms.double( 1.2 ),
      mode = cms.string( "VerticesFixed" ),
      input = cms.InputTag( "hltL1MuonsPt0" ), ## HERE
      deltaEta = cms.double( 0.35 ), # HERE
      deltaPhi = cms.double( 1.0 ), # HERE
      searchOpt = cms.bool( False ),
      whereToUseMeasurementTracker = cms.string( "ForSiStrips" ),
      originRadius = cms.double( 0.015 ),
      measurementTrackerName = cms.InputTag( "hltIter3IterL3FromL1MuonMaskedMeasurementTrackerEvent" ),
      precise = cms.bool( True )
    )
    )
    '''

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
      deltaEtas = cms.vdouble( 0.35, 0.35, 0.35, 0.35 ),
      beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
      zErrorBeamSpot = cms.double( 15.0 ), # HERE
      maxNVertices = cms.int32( 3 ), # HERE
      maxNRegions = cms.int32( 5 ),
      nSigmaZVertex = cms.double( 3.0 ),
      nSigmaZBeamSpot = cms.double( 4.0 ),
      ptMin = cms.double( 1.2 ), # HERE
      mode = cms.string( "VerticesFixed" ), # HERE
      input = cms.InputTag( "hltL1MuonsPt0" ),
      ptRanges = cms.vdouble( 0.0, 10.0, 15.0, 20.0, 1.0E64 ),
      searchOpt = cms.bool( False ),
      deltaPhis = cms.vdouble( 1.0, 0.8, 0.6, 0.3 ),
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
    MaxNumberOfCosmicClusters = cms.uint32( 50000 ),
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


# Just use TRK's DoubletRecovery dierectly
def enableDoubletRecoveryInMuon_option1(process):

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

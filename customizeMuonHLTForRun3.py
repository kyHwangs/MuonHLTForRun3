import FWCore.ParameterSet.Config as cms

def customizeMuonHLTForRun3All(process, newProcessName = "MYHLT"):

    def filters_by_type(process, type):
        return (filter for filter in process._Process__filters.values() if filter._TypedParameterizable__type == type)

    def producers_by_type(process, type):
        return (module for module in process._Process__producers.values() if module._TypedParameterizable__type == type)

    # -- Remove Iter3 (doublet)
    process.HLTIterativeTrackingIter023ForIterL3Muon = cms.Sequence(
        process.HLTIterativeTrackingIteration0ForIterL3Muon + 
        process.HLTIterativeTrackingIteration2ForIterL3Muon + 
        process.hltIter2IterL3MuonMerged
        # process.HLTIterativeTrackingIteration3ForIterL3Muon + 
        # process.hltIter3IterL3MuonMerged
    )

    process.HLTIterativeTrackingIter023ForIterL3FromL1Muon = cms.Sequence(
        process.HLTIterativeTrackingIteration0ForIterL3FromL1Muon + 
        process.HLTIterativeTrackingIteration2ForIterL3FromL1Muon + 
        process.hltIter2IterL3FromL1MuonMerged
        # process.HLTIterativeTrackingIteration3ForIterL3FromL1Muon + 
        # process.hltIter3IterL3FromL1MuonMerged
    )

    # process.hltL3MuonsIterL3IO
    for mod in producers_by_type(process, 'L3MuonProducer'):
        if hasattr(mod, 'L3TrajBuilderParameters'):
            if hasattr(mod.L3TrajBuilderParameters, 'tkTrajLabel'):
                if mod.L3TrajBuilderParameters.tkTrajLabel == cms.InputTag( "hltIter3IterL3MuonMerged" ):
                    mod.L3TrajBuilderParameters.tkTrajLabel = cms.InputTag( "hltIter2IterL3MuonMerged" )

    # process.hltIterL3MuonMerged and process.hltIterL3MuonAndMuonFromL1Merged
    for mod in producers_by_type(process, 'TrackListMerger'):
        if hasattr(mod, 'selectedTrackQuals'):
            _vinputtag = mod.selectedTrackQuals.value()
            for index in range(0, len(_vinputtag)):
                if mod.selectedTrackQuals.value()[index] == "hltIter3IterL3MuonMerged":
                    _vinputtag[index] = "hltIter2IterL3MuonMerged"
                if mod.selectedTrackQuals.value()[index] == "hltIter3IterL3FromL1MuonMerged":
                    _vinputtag[index] = "hltIter2IterL3FromL1MuonMerged"
            mod.selectedTrackQuals = cms.VInputTag( *_vinputtag )

        if hasattr(mod, 'TrackProducers'):
            _vinputtag = mod.TrackProducers.value()
            for index in range(0, len(_vinputtag)):
                if mod.TrackProducers.value()[index] == "hltIter3IterL3MuonMerged":
                    _vinputtag[index] = "hltIter2IterL3MuonMerged"
                if mod.TrackProducers.value()[index] == "hltIter3IterL3FromL1MuonMerged":
                    _vinputtag[index] = "hltIter2IterL3FromL1MuonMerged"
            mod.TrackProducers = cms.VInputTag( *_vinputtag )

    # process.hltIterL3MuonsNoID
    for mod in producers_by_type(process, 'MuonIdProducer'):
        if hasattr(mod, 'TrackExtractorPSet'):
            if hasattr(mod.TrackExtractorPSet, 'inputTrackCollection'):
                if mod.TrackExtractorPSet.inputTrackCollection == cms.InputTag( "hltIter3IterL3FromL1MuonMerged" ):
                    mod.TrackExtractorPSet.inputTrackCollection = cms.InputTag( "hltIter2IterL3FromL1MuonMerged" )

    # -- CSC segment builder
    process.hltCscSegments = cms.EDProducer( "CSCSegmentProducer",
        inputObjects = cms.InputTag( "hltCsc2DRecHits" ),
        algo_psets = cms.VPSet( 
          cms.PSet(  parameters_per_chamber_type = cms.vint32( 1, 2, 3, 4, 5, 6, 5, 6, 5, 6),
            algo_psets = cms.VPSet( 
              cms.PSet(
                        doCollisions = cms.bool(True),
                        enlarge = cms.bool(False),
                        chi2Norm_2D_ = cms.double(35),
                        chi2_str = cms.double(50.0),
                        chi2Max = cms.double(100.0),
                        dPhiIntMax = cms.double(0.005),
                        dPhiMax = cms.double(0.006),
                        wideSeg = cms.double(3.0),
                        minLayersApart = cms.int32(1),
                        dRIntMax = cms.double(2.0),
                        dRMax = cms.double(1.5)
                        ),
              cms.PSet(
                        doCollisions = cms.bool(True),
                        enlarge = cms.bool(False),
                        chi2Norm_2D_ = cms.double(35),
                        chi2_str = cms.double(50.0),
                        chi2Max = cms.double(100.0),
                        dPhiIntMax = cms.double(0.004),
                        dPhiMax = cms.double(0.005),
                        wideSeg = cms.double(3.0),
                        minLayersApart = cms.int32(1),
                        dRIntMax = cms.double(2.0),
                        dRMax = cms.double(1.5)
                        ),
              cms.PSet(
                        doCollisions = cms.bool(True),
                        enlarge = cms.bool(False),
                        chi2Norm_2D_ = cms.double(35),
                        chi2_str = cms.double(50.0),
                        chi2Max = cms.double(100.0),
                        dPhiIntMax = cms.double(0.003),
                        dPhiMax = cms.double(0.004),
                        wideSeg = cms.double(3.0),
                        minLayersApart = cms.int32(1),
                        dRIntMax = cms.double(2.0),
                        dRMax = cms.double(1.5)
                        ),
              cms.PSet(
                        doCollisions = cms.bool(True),
                        enlarge = cms.bool(False),
                        chi2Norm_2D_ = cms.double(20),
                        chi2_str = cms.double(30.0),
                        chi2Max = cms.double(60.0),
                        dPhiIntMax = cms.double(0.002),
                        dPhiMax = cms.double(0.003),
                        wideSeg = cms.double(3.0),
                        minLayersApart = cms.int32(1),
                        dRIntMax = cms.double(2.0),
                        dRMax = cms.double(1.5)
                        ),
              cms.PSet(
                        doCollisions = cms.bool(True),
                        enlarge = cms.bool(False),
                        chi2Norm_2D_ = cms.double(60),
                        chi2_str = cms.double(80.0),
                        chi2Max = cms.double(180.0),
                        dPhiIntMax = cms.double(0.005),
                        dPhiMax = cms.double(0.007),
                        wideSeg = cms.double(3.0),
                        minLayersApart = cms.int32(1),
                        dRIntMax = cms.double(2.0),
                        dRMax = cms.double(1.5)
                        ),
              cms.PSet(
                        doCollisions = cms.bool(True),
                        enlarge = cms.bool(False),
                        chi2Norm_2D_ = cms.double(35),
                        chi2_str = cms.double(50.0),
                        chi2Max = cms.double(100.0),
                        dPhiIntMax = cms.double(0.004),
                        dPhiMax = cms.double(0.006),
                        wideSeg = cms.double(3.0),
                        minLayersApart = cms.int32(1),
                        dRIntMax = cms.double(2.0),
                        dRMax = cms.double(1.5)
                        )
              ),
            algo_name = cms.string( "CSCSegAlgoRU" ),
            chamber_types = cms.vstring( 'ME1/a',
              'ME1/b',
              'ME1/2',
              'ME1/3',
              'ME2/1',
              'ME2/2',
              'ME3/1',
              'ME3/2',
              'ME4/1',
              'ME4/2' )
          )
        ),
        algo_type = cms.int32( 1 )
    )

    # -- GEM


    return process


def customizeMuonHLTForPatatrack(process, newProcessName = "MYHLT"):


    	def filters_by_type(process, type):
        	return (filter for filter in process._Process__filters.values() if filter._TypedParameterizable__type == type)

    	def producers_by_type(process, type):
        	return (module for module in process._Process__producers.values() if module._TypedParameterizable__type == type)

    	# -- modify process to create patatrack pixel tracks and vertices
	from HLTrigger.Configuration.customizeHLTforPatatrack import customizeHLTforPatatrack


	process.HLTRecoPixelTracksSequence = cms.Sequence()
	process.HLTRecopixelvertexingSequence = cms.Sequence()
	process.hltPixelTracksTrackingRegions = cms.EDProducer( "GlobalTrackingRegionFromBeamSpotEDProducer",
	    RegionPSet = cms.PSet( 
	      nSigmaZ = cms.double( 4.0 ),
	      beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
	      ptMin = cms.double( 0.8 ),
	      originRadius = cms.double( 0.02 ),
	      precise = cms.bool( True )
	    )
	)
	process.hltTrimmedPixelVertices = cms.EDProducer( "PixelVertexCollectionTrimmer",
	    src = cms.InputTag( "hltPixelVertices" ),
	    fractionSumPt2 = cms.double( 0.3 ),
	    minSumPt2 = cms.double( 0.0 ),
	    PVcomparer = cms.PSet(  refToPSet_ = cms.string( "HLTPSetPvClusterComparerForIT" ) ),
	    maxVtx = cms.uint32( 100 )
	)
	process.hltPixelTracksFitter = cms.EDProducer( "PixelFitterByHelixProjectionsProducer",
	    scaleErrorsForBPix1 = cms.bool( False ),
	    scaleFactor = cms.double( 0.65 )
	)
	process.hltPixelTracksFilter = cms.EDProducer( "PixelTrackFilterByKinematicsProducer",
	    nSigmaTipMaxTolerance = cms.double( 0.0 ),
	    chi2 = cms.double( 1000.0 ),
	    nSigmaInvPtTolerance = cms.double( 0.0 ),
	    ptMin = cms.double( 0.1 ),
	    tipMax = cms.double( 1.0 )
	)

	process = customizeHLTforPatatrack(process)    

	process.hltPixelTracksCUDA.includeJumpingForwardDoublets = cms.bool(True)
	process.hltPixelTracksCUDA.minHitsPerNtuplet             = cms.uint32(3)
	process.hltPixelTracksCUDA.idealConditions = cms.bool(True)

	process.hltPixelTracksSoA.cpu.includeJumpingForwardDoublets = cms.bool(True)
	process.hltPixelTracksSoA.cpu.minHitsPerNtuplet             = cms.uint32(3)
	process.hltPixelTracksSoA.cpu.idealConditions = cms.bool(True)

	process.hltPixelTracksInRegionL2 = cms.EDProducer("TrackSelectorByRegion",
	  produceTrackCollection = cms.bool(True),
	  produceMask = cms.bool(False),
	  tracks = cms.InputTag("hltPixelTracks"),
	  regions = cms.InputTag("hltIterL3MuonPixelTracksTrackingRegions")

	)
	process.HLTIterL3MuonRecopixelvertexingSequence = cms.Sequence( process.HLTRecopixelvertexingSequence + process.hltIterL3MuonPixelTracksTrackingRegions + process.hltPixelTracksInRegionL2 )

	process.hltIter0IterL3MuonPixelSeedsFromPixelTracks.InputCollection = cms.InputTag("hltPixelTracksInRegionL2")
	process.hltIter0IterL3MuonPixelSeedsFromPixelTracks.includeFourthHit = cms.bool(True)
	process.hltIter0IterL3MuonPixelSeedsFromPixelTracks.InputVertexCollection = cms.InputTag("hltTrimmedPixelVertices")
	process.hltIter0IterL3MuonPixelSeedsFromPixelTracks.InputVertexCollection = cms.InputTag("")

	process.hltIter0IterL3MuonTrackWithVertexSelector = cms.EDProducer("TrackWithVertexSelector",
	    # -- module configuration --
	    src = cms.InputTag('hltIter0IterL3MuonTrackSelectionHighPurity'),
	    quality = cms.string("highPurity"),
	    useVtx = cms.bool(True),
	    vertexTag = cms.InputTag('hltTrimmedPixelVertices'),
	    nVertices = cms.uint32(5),
	    zetaVtxSig = cms.double(0.3),
	    rhoVtxSig = cms.double(0.1), ## tags used by b-tagging folks
	    zetaVtx = cms.double(0.3),
	    rhoVtx = cms.double(0.1), ## tags used by b-tagging folks
	    zetaVtxScale = cms.double(1.0),
	    rhoVtxScale = cms.double(1.0), ## tags used by b-tagging folks
	    vtxFallback = cms.bool(False),
	    copyExtras = cms.untracked.bool(True),
	    copyTrajectories = cms.untracked.bool(False),
	    # --------------------------
	    # -- these are the vertex compatibility cuts --
	    # ---------------------------------------------
	    # -- dummy selection on tracks --
	    etaMin = cms.double(0.0),
	    etaMax = cms.double(5.0),
	    ptMin = cms.double(0.00001),
	    ptMax = cms.double(999999.),
	    d0Max = cms.double(999999.),
	    dzMax = cms.double(999999.),
	    normalizedChi2 = cms.double(999999.),
	    numberOfValidHits = cms.uint32(0),
	    numberOfLostHits = cms.uint32(999),
	    numberOfValidPixelHits = cms.uint32(0),
	    numberOfValidPixelHitsForGood = cms.uint32(0),
	    numberOfValidHitsForGood = cms.uint32(0),
	    timesTag = cms.InputTag(""),
	    timeResosTag = cms.InputTag(""),
	    ptErrorCut = cms.double(999999.),
	    nSigmaDtVertex = cms.double(0)
	    # ------------------------------                                       
	)

	process.hltL3MuonsIterL3IO.L3TrajBuilderParameters.tkTrajLabel = cms.InputTag("hltIter0IterL3MuonTrackWithVertexSelector")

	process.HLTIterativeTrackingIteration0ForIterL3Muon = cms.Sequence( process.hltIter0IterL3MuonPixelSeedsFromPixelTracks + process.hltIter0IterL3MuonCkfTrackCandidates + process.hltIter0IterL3MuonCtfWithMaterialTracks + process.hltIter0IterL3MuonTrackCutClassifier + process.hltIter0IterL3MuonTrackSelectionHighPurity + process.hltIter0IterL3MuonTrackWithVertexSelector)

	process.HLTIterL3IOmuonTkCandidateSequence = cms.Sequence( process.HLTIterL3MuonRecopixelvertexingSequence + process.HLTIterativeTrackingIteration0ForIterL3Muon + process.hltL3MuonsIterL3IO )


	process.hltIter0IterL3MuonTrackCutClassifier.mva.minPixelHits = cms.vint32( 0, 0, 0 )
	process.hltIter0IterL3MuonTrackCutClassifier.mva.min3DLayers = cms.vint32( 0, 0, 0 )
	process.hltIter0IterL3MuonTrackCutClassifier.vertices = cms.InputTag("hltTrimmedPixelVertices")

	process.hltPixelTracksInRegionL1 = cms.EDProducer("TrackSelectorByRegion",
	  produceTrackCollection = cms.bool(True),
	  produceMask = cms.bool(False),
	  tracks = cms.InputTag("hltPixelTracks"),
	  regions = cms.InputTag("hltIterL3FromL1MuonPixelTracksTrackingRegions")

	)
	process.HLTRecopixelvertexingSequenceForIterL3FromL1Muon = cms.Sequence( process.HLTRecopixelvertexingSequence + process.hltIterL3FromL1MuonPixelTracksTrackingRegions + process.hltPixelTracksInRegionL1 )
	process.hltIterL3FromL1MuonPixelVertices.TrackCollection = cms.InputTag("hltPixelTracks")

	process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks.InputCollection = cms.InputTag("hltPixelTracksInRegionL1")
	process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks.InputVertexCollection = cms.InputTag("")
	process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks.includeFourthHit = cms.bool(True)


	process.hltIter0IterL3FromL1MuonTrackWithVertexSelector = cms.EDProducer("TrackWithVertexSelector",
	    # -- module configuration --
	    src = cms.InputTag('hltIter0IterL3FromL1MuonTrackSelectionHighPurity'),
	    quality = cms.string("highPurity"),
	    useVtx = cms.bool(True),
	    vertexTag = cms.InputTag('hltTrimmedPixelVertices'),
	    nVertices = cms.uint32(5),
	    vtxFallback = cms.bool(False),
	    zetaVtx = cms.double(0.3),
	    zetaVtxScale = cms.double(1.0),
	    rhoVtxScale = cms.double(1.0), ## tags used by b-tagging folks
	    rhoVtx = cms.double(0.1), ## tags used by b-tagging folks
	    rhoVtxSig = cms.double(0.1), ## tags used by b-tagging folks
	    zetaVtxSig = cms.double(0.3),
	    copyExtras = cms.untracked.bool(True),
	    copyTrajectories = cms.untracked.bool(False),
	    # --------------------------
	    # -- these are the vertex compatibility cuts --
	    # ---------------------------------------------
	    # -- dummy selection on tracks --
	    etaMin = cms.double(0.0),
	    etaMax = cms.double(5.0),
	    ptMin = cms.double(0.00001),
	    ptMax = cms.double(999999.),
	    d0Max = cms.double(999999.),
	    dzMax = cms.double(999999.),
	    normalizedChi2 = cms.double(999999.),
	    numberOfValidHits = cms.uint32(0),
	    numberOfLostHits = cms.uint32(999),
	    numberOfValidPixelHits = cms.uint32(0),
	    numberOfValidPixelHitsForGood = cms.uint32(0),
	    numberOfValidHitsForGood = cms.uint32(0),
	    timesTag = cms.InputTag(""),
	    timeResosTag = cms.InputTag(""),
	    ptErrorCut = cms.double(999999.),
	    nSigmaDtVertex = cms.double(0),
	    # ------------------------------                                       
	)

	process.HLTIterativeTrackingIteration0ForIterL3FromL1Muon = cms.Sequence( process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks + process.hltIter0IterL3FromL1MuonCkfTrackCandidates + process.hltIter0IterL3FromL1MuonCtfWithMaterialTracks + process.hltIter0IterL3FromL1MuonTrackCutClassifier + process.hltIter0IterL3FromL1MuonTrackSelectionHighPurity + process.hltIter0IterL3FromL1MuonTrackWithVertexSelector )

	process.HLTIterL3IOmuonFromL1TkCandidateSequence = cms.Sequence( process.HLTRecopixelvertexingSequenceForIterL3FromL1Muon + process.HLTIterativeTrackingIteration0ForIterL3FromL1Muon )

	process.hltIter0IterL3FromL1MuonTrackCutClassifier.mva.minPixelHits = cms.vint32( 0, 0, 0 )
	process.hltIter0IterL3FromL1MuonTrackCutClassifier.mva.min3DLayers = cms.vint32( 0, 0, 0 )
	process.hltIter0IterL3FromL1MuonTrackCutClassifier.vertices = cms.InputTag("hltTrimmedPixelVertices")

	process.hltIterL3MuonMerged.selectedTrackQuals = cms.VInputTag( 'hltIterL3OIMuonTrackSelectionHighPurity','hltIter0IterL3MuonTrackWithVertexSelector' )
	process.hltIterL3MuonMerged.TrackProducers = cms.VInputTag( 'hltIterL3OIMuonTrackSelectionHighPurity','hltIter0IterL3MuonTrackWithVertexSelector' )

	process.hltIterL3MuonAndMuonFromL1Merged.selectedTrackQuals = cms.VInputTag( 'hltIterL3MuonMerged','hltIter0IterL3FromL1MuonTrackWithVertexSelector' )
	process.hltIterL3MuonAndMuonFromL1Merged.TrackProducers = cms.VInputTag( 'hltIterL3MuonMerged','hltIter0IterL3FromL1MuonTrackWithVertexSelector' )

	process.hltIterL3MuonsNoID.inputTrackCollection = cms.InputTag( "hltIter0IterL3FromL1MuonTrackWithVertexSelector")


	return process


def customizeMuonHLTForPatatrackGlobal(process, newProcessName = "MYHLT"):


    	def filters_by_type(process, type):
        	return (filter for filter in process._Process__filters.values() if filter._TypedParameterizable__type == type)

    	def producers_by_type(process, type):
        	return (module for module in process._Process__producers.values() if module._TypedParameterizable__type == type)

    	# -- modify process to create patatrack pixel tracks and vertices
	from HLTrigger.Configuration.customizeHLTforPatatrack import customizeHLTforPatatrack


	process.HLTRecoPixelTracksSequence = cms.Sequence()
	process.HLTRecopixelvertexingSequence = cms.Sequence()
	process.hltPixelTracksTrackingRegions = cms.EDProducer( "GlobalTrackingRegionFromBeamSpotEDProducer",
	    RegionPSet = cms.PSet( 
	      nSigmaZ = cms.double( 4.0 ),
	      beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
	      ptMin = cms.double( 0.8 ),
	      originRadius = cms.double( 0.02 ),
	      precise = cms.bool( True )
	    )
	)
	process.hltTrimmedPixelVertices = cms.EDProducer( "PixelVertexCollectionTrimmer",
	    src = cms.InputTag( "hltPixelVertices" ),
	    fractionSumPt2 = cms.double( 0.3 ),
	    minSumPt2 = cms.double( 0.0 ),
	    PVcomparer = cms.PSet(  refToPSet_ = cms.string( "HLTPSetPvClusterComparerForIT" ) ),
	    maxVtx = cms.uint32( 100 )
	)
	process.hltPixelTracksFitter = cms.EDProducer( "PixelFitterByHelixProjectionsProducer",
	    scaleErrorsForBPix1 = cms.bool( False ),
	    scaleFactor = cms.double( 0.65 )
	)
	process.hltPixelTracksFilter = cms.EDProducer( "PixelTrackFilterByKinematicsProducer",
	    nSigmaTipMaxTolerance = cms.double( 0.0 ),
	    chi2 = cms.double( 1000.0 ),
	    nSigmaInvPtTolerance = cms.double( 0.0 ),
	    ptMin = cms.double( 0.1 ),
	    tipMax = cms.double( 1.0 )
	)

	process = customizeHLTforPatatrack(process)    

	process.hltPixelTracksCUDA.includeJumpingForwardDoublets = cms.bool(True)
	process.hltPixelTracksCUDA.minHitsPerNtuplet             = cms.uint32(3)
	process.hltPixelTracksCUDA.idealConditions = cms.bool(True)

	process.hltPixelTracksSoA.cpu.includeJumpingForwardDoublets = cms.bool(True)
	process.hltPixelTracksSoA.cpu.minHitsPerNtuplet             = cms.uint32(3)
	process.hltPixelTracksSoA.cpu.idealConditions = cms.bool(True)

	process.HLTIterL3MuonRecopixelvertexingSequence = cms.Sequence( process.HLTRecopixelvertexingSequence + process.hltIterL3MuonPixelTracksTrackingRegions )

	process.hltIter0IterL3MuonPixelSeedsFromPixelTracks.InputCollection = cms.InputTag("hltPixelTracks")
	process.hltIter0IterL3MuonPixelSeedsFromPixelTracks.includeFourthHit = cms.bool(True)
	process.hltIter0IterL3MuonPixelSeedsFromPixelTracks.InputVertexCollection = cms.InputTag("hltTrimmedPixelVertices")
	process.hltIter0IterL3MuonPixelSeedsFromPixelTracks.InputVertexCollection = cms.InputTag("")

	process.hltIter0IterL3MuonTrackWithVertexSelector = cms.EDProducer("TrackWithVertexSelector",
	    # -- module configuration --
	    src = cms.InputTag('hltIter0IterL3MuonTrackSelectionHighPurity'),
	    quality = cms.string("highPurity"),
	    useVtx = cms.bool(True),
	    vertexTag = cms.InputTag('hltTrimmedPixelVertices'),
	    nVertices = cms.uint32(5),
	    zetaVtxSig = cms.double(0.3),
	    rhoVtxSig = cms.double(0.1), ## tags used by b-tagging folks
	    zetaVtx = cms.double(0.3),
	    rhoVtx = cms.double(0.1), ## tags used by b-tagging folks
	    zetaVtxScale = cms.double(1.0),
	    rhoVtxScale = cms.double(1.0), ## tags used by b-tagging folks
	    vtxFallback = cms.bool(False),
	    copyExtras = cms.untracked.bool(True),
	    copyTrajectories = cms.untracked.bool(False),
	    # --------------------------
	    # -- these are the vertex compatibility cuts --
	    # ---------------------------------------------
	    # -- dummy selection on tracks --
	    etaMin = cms.double(0.0),
	    etaMax = cms.double(5.0),
	    ptMin = cms.double(0.00001),
	    ptMax = cms.double(999999.),
	    d0Max = cms.double(999999.),
	    dzMax = cms.double(999999.),
	    normalizedChi2 = cms.double(999999.),
	    numberOfValidHits = cms.uint32(0),
	    numberOfLostHits = cms.uint32(999),
	    numberOfValidPixelHits = cms.uint32(0),
	    numberOfValidPixelHitsForGood = cms.uint32(0),
	    numberOfValidHitsForGood = cms.uint32(0),
	    timesTag = cms.InputTag(""),
	    timeResosTag = cms.InputTag(""),
	    ptErrorCut = cms.double(999999.),
	    nSigmaDtVertex = cms.double(0)
	    # ------------------------------                                       
	)

	process.hltL3MuonsIterL3IO.L3TrajBuilderParameters.tkTrajLabel = cms.InputTag("hltIter0IterL3MuonTrackWithVertexSelector")

	process.HLTIterativeTrackingIteration0ForIterL3Muon = cms.Sequence( process.hltIter0IterL3MuonPixelSeedsFromPixelTracks + process.hltIter0IterL3MuonCkfTrackCandidates + process.hltIter0IterL3MuonCtfWithMaterialTracks + process.hltIter0IterL3MuonTrackCutClassifier + process.hltIter0IterL3MuonTrackSelectionHighPurity + process.hltIter0IterL3MuonTrackWithVertexSelector)

	process.HLTIterL3IOmuonTkCandidateSequence = cms.Sequence( process.HLTIterL3MuonRecopixelvertexingSequence + process.HLTIterativeTrackingIteration0ForIterL3Muon + process.hltL3MuonsIterL3IO )


	process.hltIter0IterL3MuonTrackCutClassifier.mva.minPixelHits = cms.vint32( 0, 0, 0 )
	process.hltIter0IterL3MuonTrackCutClassifier.mva.min3DLayers = cms.vint32( 0, 0, 0 )
	process.hltIter0IterL3MuonTrackCutClassifier.vertices = cms.InputTag("hltTrimmedPixelVertices")

	process.HLTRecopixelvertexingSequenceForIterL3FromL1Muon = cms.Sequence( process.HLTRecopixelvertexingSequence + process.hltIterL3FromL1MuonPixelTracksTrackingRegions )
	process.hltIterL3FromL1MuonPixelVertices.TrackCollection = cms.InputTag("hltPixelTracks")

	process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks.InputCollection = cms.InputTag("hltPixelTracks")
	process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks.InputVertexCollection = cms.InputTag("")
	process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks.includeFourthHit = cms.bool(True)


	process.hltIter0IterL3FromL1MuonTrackWithVertexSelector = cms.EDProducer("TrackWithVertexSelector",
	    # -- module configuration --
	    src = cms.InputTag('hltIter0IterL3FromL1MuonTrackSelectionHighPurity'),
	    quality = cms.string("highPurity"),
	    useVtx = cms.bool(True),
	    vertexTag = cms.InputTag('hltTrimmedPixelVertices'),
	    nVertices = cms.uint32(5),
	    vtxFallback = cms.bool(False),
	    zetaVtx = cms.double(0.3),
	    zetaVtxScale = cms.double(1.0),
	    rhoVtxScale = cms.double(1.0), ## tags used by b-tagging folks
	    rhoVtx = cms.double(0.1), ## tags used by b-tagging folks
	    rhoVtxSig = cms.double(0.1), ## tags used by b-tagging folks
	    zetaVtxSig = cms.double(0.3),
	    copyExtras = cms.untracked.bool(True),
	    copyTrajectories = cms.untracked.bool(False),
	    # --------------------------
	    # -- these are the vertex compatibility cuts --
	    # ---------------------------------------------
	    # -- dummy selection on tracks --
	    etaMin = cms.double(0.0),
	    etaMax = cms.double(5.0),
	    ptMin = cms.double(0.00001),
	    ptMax = cms.double(999999.),
	    d0Max = cms.double(999999.),
	    dzMax = cms.double(999999.),
	    normalizedChi2 = cms.double(999999.),
	    numberOfValidHits = cms.uint32(0),
	    numberOfLostHits = cms.uint32(999),
	    numberOfValidPixelHits = cms.uint32(0),
	    numberOfValidPixelHitsForGood = cms.uint32(0),
	    numberOfValidHitsForGood = cms.uint32(0),
	    timesTag = cms.InputTag(""),
	    timeResosTag = cms.InputTag(""),
	    ptErrorCut = cms.double(999999.),
	    nSigmaDtVertex = cms.double(0),
	    # ------------------------------                                       
	)

	process.HLTIterativeTrackingIteration0ForIterL3FromL1Muon = cms.Sequence( process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks + process.hltIter0IterL3FromL1MuonCkfTrackCandidates + process.hltIter0IterL3FromL1MuonCtfWithMaterialTracks + process.hltIter0IterL3FromL1MuonTrackCutClassifier + process.hltIter0IterL3FromL1MuonTrackSelectionHighPurity + process.hltIter0IterL3FromL1MuonTrackWithVertexSelector )

	process.HLTIterL3IOmuonFromL1TkCandidateSequence = cms.Sequence( process.HLTRecopixelvertexingSequenceForIterL3FromL1Muon + process.HLTIterativeTrackingIteration0ForIterL3FromL1Muon )

	process.hltIter0IterL3FromL1MuonTrackCutClassifier.mva.minPixelHits = cms.vint32( 0, 0, 0 )
	process.hltIter0IterL3FromL1MuonTrackCutClassifier.mva.min3DLayers = cms.vint32( 0, 0, 0 )
	process.hltIter0IterL3FromL1MuonTrackCutClassifier.vertices = cms.InputTag("hltTrimmedPixelVertices")

	process.hltIterL3MuonMerged.selectedTrackQuals = cms.VInputTag( 'hltIterL3OIMuonTrackSelectionHighPurity','hltIter0IterL3MuonTrackWithVertexSelector' )
	process.hltIterL3MuonMerged.TrackProducers = cms.VInputTag( 'hltIterL3OIMuonTrackSelectionHighPurity','hltIter0IterL3MuonTrackWithVertexSelector' )

	process.hltIterL3MuonAndMuonFromL1Merged.selectedTrackQuals = cms.VInputTag( 'hltIterL3MuonMerged','hltIter0IterL3FromL1MuonTrackWithVertexSelector' )
	process.hltIterL3MuonAndMuonFromL1Merged.TrackProducers = cms.VInputTag( 'hltIterL3MuonMerged','hltIter0IterL3FromL1MuonTrackWithVertexSelector' )

	process.hltIterL3MuonsNoID.inputTrackCollection = cms.InputTag( "hltIter0IterL3FromL1MuonTrackWithVertexSelector")


	return process

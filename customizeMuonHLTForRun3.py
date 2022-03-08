import FWCore.ParameterSet.Config as cms

from HLTrigger.Configuration.common import *

def customizeMuonHLTForDoubletRemoval(process, newProcessName = "MYHLT"):
    if not hasattr(process, "HLTIterativeTrackingIter023ForIterL3Muon") or\
       not hasattr(process, "HLTIterativeTrackingIter023ForIterL3FromL1Muon"):
        return process

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

    return process


def customizeMuonHLTForCscSegment(process, newProcessName = "MYHLT"):
    if not hasattr(process, "hltCscSegments"):
        return process

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

    return process


def customizeMuonHLTForGEM(process, newProcessName = "MYHLT"):

	if 'HLTMuonLocalRecoSequence' not in process.__dict__.keys():
		return process

	process.load('Geometry.GEMGeometryBuilder.gemGeometryDB_cfi')

	# GEM local reco (from offline)
	from Configuration.StandardSequences.RawToDigi_cff import muonGEMDigis
	from Configuration.StandardSequences.Reconstruction_cff import gemRecHits, gemSegments

	process.hltMuonGEMDigis = muonGEMDigis.clone()

	process.hltGemRecHits = gemRecHits.clone(
		gemDigiLabel = cms.InputTag("hltMuonGEMDigis"),
	)

	process.hltGemSegments = gemSegments.clone(
		gemRecHitLabel = cms.InputTag("hltGemRecHits")
	)

	process.HLTMuonLocalRecoSequence = cms.Sequence(
		process.hltMuonDTDigis +
		process.hltDt1DRecHits +
		process.hltDt4DSegments +
		process.hltMuonCSCDigis +
		process.hltCsc2DRecHits +
		process.hltCscSegments +
		process.hltMuonRPCDigis +
		process.hltRpcRecHits +
		process.hltMuonGEMDigis +
		process.hltGemRecHits +
		process.hltGemSegments
	)

	# L2 reconstruction
	if hasattr(process, "hltL2Muons"):
		process.hltL2Muons.L2TrajBuilderParameters.FilterParameters.EnableGEMMeasurement = cms.bool(True)
		process.hltL2Muons.L2TrajBuilderParameters.FilterParameters.GEMRecSegmentLabel = cms.InputTag("hltGemRecHits")
		process.hltL2Muons.L2TrajBuilderParameters.BWFilterParameters.EnableGEMMeasurement = cms.bool(True)
		process.hltL2Muons.L2TrajBuilderParameters.BWFilterParameters.GEMRecSegmentLabel = cms.InputTag("hltGemRecHits")

	# L3 reconstruction
	if hasattr(process, "hltL3MuonsIterL3OI"):
		process.hltL3MuonsIterL3OI.L3TrajBuilderParameters.GlbRefitterParameters.GEMRecHitLabel = cms.InputTag("hltGemRecHits" )
		process.hltL3MuonsIterL3OI.L3TrajBuilderParameters.GlbRefitterParameters.Chi2CutGEM = cms.double(1.0)

	if hasattr(process, "hltL3MuonsIterL3IO"):
		process.hltL3MuonsIterL3IO.L3TrajBuilderParameters.GlbRefitterParameters.GEMRecHitLabel = cms.InputTag("hltGemRecHits")
		process.hltL3MuonsIterL3IO.L3TrajBuilderParameters.GlbRefitterParameters.Chi2CutGEM = cms.double(1.0)

	if hasattr(process, "hltIterL3GlbMuon"):
		process.hltIterL3GlbMuon.L3TrajBuilderParameters.GlbRefitterParameters.GEMRecHitLabel = cms.InputTag("hltGemRecHits")
		process.hltIterL3GlbMuon.L3TrajBuilderParameters.GlbRefitterParameters.Chi2CutGEM = cms.double(1.0)

	if hasattr(process, "hltIterL3MuonsNoID"):
		process.hltIterL3MuonsNoID.TrackAssociatorParameters.useGEM = cms.bool(True)
		process.hltIterL3MuonsNoID.TrackAssociatorParameters.GEMSegmentCollectionLabel = cms.InputTag("hltGemSegments")

	return process


def customizeMuonHLTForPatatrackWithIsoAndTriplets(process, loadPatatrack=False, newProcessName = "MYHLT", IOROIFactor = 1.5):
	if loadPatatrack:
    	# -- modify process to create patatrack pixel tracks and vertices
		from HLTrigger.Configuration.customizeHLTforPatatrack import customizeHLTforPatatrackTriplets


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
	 
		process = customizeHLTforPatatrackTriplets(process)    

	if hasattr(process, "HLTL3muonrecoNocandSequence"):
		process.hltPixelTracksInRegionL2 = cms.EDProducer("TrackSelectorByRegion",
		  produceTrackCollection = cms.bool(True),
		  produceMask = cms.bool(False),
		  tracks = cms.InputTag("hltPixelTracks"),
		  regions = cms.InputTag("hltIterL3MuonPixelTracksTrackingRegions")

		)

		process.hltIterL3MuonPixelTracksTrackingRegions.Pt_min = 0.0 
		process.hltIterL3MuonPixelTracksTrackingRegions.maxRegions = 5 

		# ROI size
		process.hltIterL3MuonPixelTracksTrackingRegions.DeltaEta = 0.2 * IOROIFactor
		process.hltIterL3MuonPixelTracksTrackingRegions.DeltaPhi = 0.15 * IOROIFactor

		process.HLTIterL3MuonRecopixelvertexingSequence = cms.Sequence( process.HLTRecopixelvertexingSequence + process.hltIterL3MuonPixelTracksTrackingRegions + process.hltPixelTracksInRegionL2 )

		process.hltIter0IterL3MuonPixelSeedsFromPixelTracks.InputCollection = "hltPixelTracksInRegionL2"
		process.hltIter0IterL3MuonPixelSeedsFromPixelTracks.includeFourthHit = True
		process.hltIter0IterL3MuonPixelSeedsFromPixelTracks.InputVertexCollection =  ""


		process.HLTIterativeTrackingIteration0ForIterL3Muon = cms.Sequence( process.hltIter0IterL3MuonPixelSeedsFromPixelTracks + process.hltIter0IterL3MuonCkfTrackCandidates + process.hltIter0IterL3MuonCtfWithMaterialTracks + process.hltIter0IterL3MuonTrackCutClassifier + process.hltIter0IterL3MuonTrackSelectionHighPurity)

		process.hltL3MuonsIterL3IO.L3TrajBuilderParameters.tkTrajLabel = "hltIter0IterL3MuonTrackSelectionHighPurity"
		process.hltL3MuonsIterL3IO.L3TrajBuilderParameters.tkTrajVertex = "hltTrimmedPixelVertices"

		process.HLTIterL3IOmuonTkCandidateSequence = cms.Sequence( process.HLTIterL3MuonRecopixelvertexingSequence + process.HLTIterativeTrackingIteration0ForIterL3Muon + process.hltL3MuonsIterL3IO )

		process.hltIter0IterL3MuonTrackCutClassifier.vertices = "hltTrimmedPixelVertices"
		process.hltIter0IterL3MuonTrackCutClassifier.mva.minPixelHits = [ 0, 0, 0 ]
		process.hltIter0IterL3MuonTrackCutClassifier.mva.min3DLayers = [0, 0, 0 ]


		process.hltPixelTracksInRegionL1 = cms.EDProducer("TrackSelectorByRegion",
		  produceTrackCollection = cms.bool(True),
		  produceMask = cms.bool(False),
		  tracks = cms.InputTag("hltPixelTracks"),
		  regions = cms.InputTag("hltIterL3FromL1MuonPixelTracksTrackingRegions")

		)

		process.hltIterL3FromL1MuonPixelTracksTrackingRegions.RegionPSet.ptMin = 0.0 
		process.hltIterL3FromL1MuonPixelTracksTrackingRegions.RegionPSet.maxNRegions = 5 

		# ROI size
		process.hltIterL3FromL1MuonPixelTracksTrackingRegions.RegionPSet.deltaEta = 0.35 * IOROIFactor
		process.hltIterL3FromL1MuonPixelTracksTrackingRegions.RegionPSet.deltaPhi = 0.2  * IOROIFactor

		process.HLTRecopixelvertexingSequenceForIterL3FromL1Muon = cms.Sequence( process.HLTRecopixelvertexingSequence + process.hltIterL3FromL1MuonPixelTracksTrackingRegions + process.hltPixelTracksInRegionL1 )

		process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks.InputCollection = "hltPixelTracksInRegionL1"
		process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks.InputVertexCollection = ""
		process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks.includeFourthHit = True


		process.HLTIterativeTrackingIteration0ForIterL3FromL1Muon = cms.Sequence( process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks + process.hltIter0IterL3FromL1MuonCkfTrackCandidates + process.hltIter0IterL3FromL1MuonCtfWithMaterialTracks + process.hltIter0IterL3FromL1MuonTrackCutClassifier + process.hltIter0IterL3FromL1MuonTrackSelectionHighPurity )

		process.HLTIterL3IOmuonFromL1TkCandidateSequence = cms.Sequence( process.HLTRecopixelvertexingSequenceForIterL3FromL1Muon + process.HLTIterativeTrackingIteration0ForIterL3FromL1Muon )

		process.hltIter0IterL3FromL1MuonTrackCutClassifier.vertices = "hltTrimmedPixelVertices"
		process.hltIter0IterL3FromL1MuonTrackCutClassifier.mva.minPixelHits = [0, 0, 0]
		process.hltIter0IterL3FromL1MuonTrackCutClassifier.mva.min3DLayers = [0, 0, 0]


		process.hltIterL3MuonMerged.selectedTrackQuals = ['hltIterL3OIMuonTrackSelectionHighPurity','hltIter0IterL3MuonTrackSelectionHighPurity']
		process.hltIterL3MuonMerged.TrackProducers = ['hltIterL3OIMuonTrackSelectionHighPurity','hltIter0IterL3MuonTrackSelectionHighPurity']

		process.hltIterL3MuonAndMuonFromL1Merged.selectedTrackQuals = ['hltIterL3MuonMerged','hltIter0IterL3FromL1MuonTrackSelectionHighPurity']
		process.hltIterL3MuonAndMuonFromL1Merged.TrackProducers = ['hltIterL3MuonMerged','hltIter0IterL3FromL1MuonTrackSelectionHighPurity']

		process.hltIterL3MuonsNoID.TrackExtractorPSet.inputTrackCollection = "hltIter0IterL3FromL1MuonTrackSelectionHighPurity"
	# the tracker isolatin part
	if hasattr(process, "HLTIterativeTrackingL3MuonIteration0"):
		process.hltPixelTracksTrackingRegionsForSeedsL3Muon.RegionPSet.ptMin = 0.3
		process.hltPixelTracksTrackingRegionsForSeedsL3Muon.RegionPSet.vertexCollection = "hltPixelVertices"

		process.hltPixelTracksInRegionIter0L3Muon = cms.EDProducer("TrackSelectorByRegion",
	          produceTrackCollection = cms.bool(True),
	          produceMask = cms.bool(False),
	          tracks = cms.InputTag("hltPixelTracks"),
	          regions = cms.InputTag("hltPixelTracksTrackingRegionsForSeedsL3Muon")

	        )
		process.hltIter0L3MuonPixelSeedsFromPixelTracks.InputCollection = "hltPixelTracksInRegionIter0L3Muon"
		process.hltIter0L3MuonPixelSeedsFromPixelTracks.InputVertexCollection = "hltPixelVertices"
		process.hltIter0L3MuonTrackCutClassifier.vertices = "hltPixelVertices"

		process.HLTIterativeTrackingL3MuonIteration0 = cms.Sequence( process.hltPixelTracksTrackingRegionsForSeedsL3Muon + process.hltPixelTracksInRegionIter0L3Muon + process.hltIter0L3MuonPixelSeedsFromPixelTracks + process.hltIter0L3MuonCkfTrackCandidates + process.hltIter0L3MuonCtfWithMaterialTracks + process.hltIter0L3MuonTrackCutClassifier + process.hltIter0L3MuonTrackSelectionHighPurity )

		if hasattr(process, "HLTTrackReconstructionForIsoL3MuonIter02"):
			process.HLTTrackReconstructionForIsoL3MuonIter02 = cms.Sequence( process.HLTDoLocalPixelSequence + process.HLTDoLocalStripSequence + process.HLTIterativeTrackingL3MuonIteration0 )
			if hasattr(process, "hltMuonTkRelIsolationCut0p07Map"):
				process.hltMuonTkRelIsolationCut0p07Map.TrkExtractorPSet.inputTrackCollection = "hltIter0L3MuonTrackSelectionHighPurity"
			if hasattr(process, "hltL3MuonCombRelIsolationVVVL"):
				process.hltL3MuonCombRelIsolationVVVL.TrkExtractorPSet.inputTrackCollection = "hltIter0L3MuonTrackSelectionHighPurity"

		if hasattr(process, "HLTL3muontrkisorecoSequence"):
			process.HLTL3muontrkisorecoSequence = cms.Sequence( process.HLTDoLocalPixelSequence + process.HLTDoLocalStripSequence + process.HLTIterativeTrackingL3MuonIteration0 )
			if hasattr(process, "hltL3MuonRelTrkIsolationVVL"):
				process.hltL3MuonRelTrkIsolationVVL.TrkExtractorPSet.inputTrackCollection = "hltIter0L3MuonTrackSelectionHighPurity"
			if hasattr(process, "hltTauPt15MuPts711Mass1p3to2p1IsoCharge1"):
				process.hltTauPt15MuPts711Mass1p3to2p1IsoCharge1.IsoTracksSrc = "hltIter0L3MuonTrackSelectionHighPurity"
			if hasattr(process, "hltTauPt15MuPts711Mass1p3to2p1Iso"):
				process.hltTauPt15MuPts711Mass1p3to2p1Iso.IsoTracksSrc = "hltIter0L3MuonTrackSelectionHighPurity"

	return process


def customizeMuonHLTForPatatrackTkMu(process, loadPatatrack=False, newProcessName = "MYHLT"):
	if loadPatatrack:
    	# -- modify process to create patatrack pixel tracks and vertices
		from HLTrigger.Configuration.customizeHLTforPatatrack import customizeHLTforPatatrackTriplets


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
	 
		process = customizeHLTforPatatrackTriplets(process)    

	if hasattr(process, "HLTIterativeTrackingHighPtTkMu"):
		process.hltPixelTracksInRegionTkMu = cms.EDProducer("TrackSelectorByRegion",
		  produceTrackCollection = cms.bool(True),
		  produceMask = cms.bool(False),
		  tracks = cms.InputTag("hltPixelTracks"),
		  regions = cms.InputTag("hltIter0HighPtTkMuPixelTracksTrackingRegions")

		)

		process.hltIter0HighPtTkMuPixelTracksTrackingRegions.RegionPSet.ptMin = 10.0
		process.hltIter0HighPtTkMuPixelTracksTrackingRegions.RegionPSet.maxNRegions = 5


		process.hltIter0HighPtTkMuPixelSeedsFromPixelTracks.InputCollection = "hltPixelTracksInRegionTkMu"
		process.hltIter0HighPtTkMuPixelSeedsFromPixelTracks.includeFourthHit = True

		process.HLTIterativeTrackingHighPtTkMuIteration0 = cms.Sequence(process.hltIter0HighPtTkMuPixelTracksTrackingRegions + process.hltPixelTracksInRegionTkMu + process.hltIter0HighPtTkMuPixelSeedsFromPixelTracks + process.hltIter0HighPtTkMuCkfTrackCandidates + process.hltIter0HighPtTkMuCtfWithMaterialTracks + process.hltIter0HighPtTkMuTrackSelectionHighPurity )


		process.HLTIterativeTrackingHighPtTkMu = cms.Sequence(process.HLTIterativeTrackingHighPtTkMuIteration0)

	if hasattr(process, "hltHighPtTkMu50TkFilt"):
		process.hltHighPtTkMu50TkFilt.src = "hltIter0HighPtTkMuTrackSelectionHighPurity"
	if hasattr(process, "hltHighPtTkMuons"):
		process.hltHighPtTkMuons.inputCollectionLabels = ['hltIter0HighPtTkMuTrackSelectionHighPurity']


	if hasattr(process, "HLTTrackerMuonSequenceLowPtIter0and1"):
		process.HLTTrackerMuonSequenceLowPtIter0and1 = cms.Sequence( process.HLTDoLocalPixelSequence + process.HLTRecopixelvertexingSequence + process.HLTDoLocalStripSequence + process.HLTIterativeTrackingIteration0 + process.HLTL3muonrecoNocandSequence + process.hltDiMuonMergingIter01TkMu + process.hltDiMuonLinksIter01TkMuMerge + process.hltGlbTrkMuonsLowPtIter01Merge + process.hltGlbTrkMuonLowPtIter01MergeCands )
		process.hltDiMuonMergingIter01TkMu.TrackProducers = ['hltIterL3MuonAndMuonFromL1Merged','hltMergedTracks'] #probably unnecessary
		process.hltDiMuonMergingIter01TkMu.selectedTrackQuals = ['hltIterL3MuonAndMuonFromL1Merged','hltMergedTracks'] # "" 

	if hasattr(process, "HLTTrackerMuonSequenceLowPt"):
		process.HLTTrackerMuonSequenceLowPt = cms.Sequence( process.HLTDoLocalPixelSequence + process.HLTRecopixelvertexingSequence + process.HLTDoLocalStripSequence + process.HLTIterativeTrackingIteration0 + process.HLTL3muonrecoNocandSequence + process.hltDiMuonMergingIter01TkMu + process.hltDiMuonLinksIter01TkMuMerge + process.hltGlbTrkMuonsLowPtIter01Merge + process.hltGlbTrkMuonLowPtIter01MergeCands )

	return process


def customizeMuonHLTForPatatrackNoVtx(process, loadPatatrack=False, newProcessName = "MYHLT"):
	if not hasattr(process, "HLTL3muonrecoNocandSequenceNoVtx"):
		return process

	if loadPatatrack:
    	# -- modify process to create patatrack pixel tracks and vertices
		from HLTrigger.Configuration.customizeHLTforPatatrack import customizeHLTforPatatrackTriplets


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
	 
		process = customizeHLTforPatatrackTriplets(process)    

	process.hltPixelTracksInRegionL2NoVtx = cms.EDProducer("TrackSelectorByRegion",
	  produceTrackCollection = cms.bool(True),
	  produceMask = cms.bool(False),
	  tracks = cms.InputTag("hltPixelTracks"),
	  regions = cms.InputTag("hltIterL3MuonPixelTracksTrackingRegionsNoVtx")

	)

	process.hltIterL3MuonPixelTracksTrackingRegionsNoVtx.Pt_min = 0.0


	process.HLTIterL3MuonRecoPixelTracksSequenceNoVtx = cms.Sequence( process.HLTRecopixelvertexingSequence + process.hltIterL3MuonPixelTracksTrackingRegionsNoVtx + process.hltPixelTracksInRegionL2NoVtx )
	process.HLTIterL3MuonRecopixelvertexingSequenceNoVtx = cms.Sequence( process.HLTIterL3MuonRecoPixelTracksSequenceNoVtx )
	process.hltIter0IterL3MuonPixelSeedsFromPixelTracksNoVtx.InputCollection = "hltPixelTracksInRegionL2NoVtx"
	process.hltIter0IterL3MuonPixelSeedsFromPixelTracksNoVtx.includeFourthHit = True
	process.hltIter0IterL3MuonPixelSeedsFromPixelTracksNoVtx.InputVertexCollection = ""


	process.HLTIterL3IOmuonTkCandidateSequenceNoVtx = cms.Sequence( process.HLTIterL3MuonRecopixelvertexingSequenceNoVtx + process.HLTIterativeTrackingIteration0ForIterL3MuonNoVtx + process.hltL3MuonsIterL3IONoVtx )

	process.hltIter0IterL3MuonTrackCutClassifierNoVtx.vertices = "hltTrimmedPixelVertices"
	process.hltIter0IterL3MuonTrackCutClassifierNoVtx.mva.minPixelHits = [0, 0, 0]
	process.hltIter0IterL3MuonTrackCutClassifierNoVtx.mva.min3DLayers = [0, 0, 0]


	process.hltL3MuonsIterL3IONoVtx.L3TrajBuilderParameters.tkTrajLabel = "hltIter0IterL3MuonTrackSelectionHighPurityNoVtx"
	process.hltL3MuonsIterL3IONoVtx.L3TrajBuilderParameters.tkTrajVertex = "hltTrimmedPixelVertices"

	process.hltPixelTracksInRegionL1NoVtx = cms.EDProducer("TrackSelectorByRegion",
	  produceTrackCollection = cms.bool(True),
	  produceMask = cms.bool(False),
	  tracks = cms.InputTag("hltPixelTracks"),
	  regions = cms.InputTag("hltIterL3FromL1MuonPixelTracksTrackingRegionsNoVtx")

	)

	process.hltIterL3FromL1MuonPixelTracksTrackingRegionsNoVtx.RegionPSet.ptMin = 0.0
	process.hltIterL3FromL1MuonPixelTracksTrackingRegionsNoVtx.RegionPSet.maxNRegions = 5

	process.HLTRecopixelvertexingSequenceForIterL3FromL1MuonNoVtx = cms.Sequence( process.HLTRecopixelvertexingSequence + process.hltIterL3FromL1MuonPixelTracksTrackingRegionsNoVtx + process.hltPixelTracksInRegionL1NoVtx )

	process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksNoVtx.InputCollection = "hltPixelTracksInRegionL1NoVtx"
	process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksNoVtx.InputVertexCollection = ""
	process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksNoVtx.includeFourthHit = True

	process.HLTIterL3IOmuonFromL1TkCandidateSequenceNoVtx = cms.Sequence( process.HLTRecopixelvertexingSequenceForIterL3FromL1MuonNoVtx + process.HLTIterativeTrackingIteration0ForIterL3FromL1MuonNoVtx )

	process.hltIter0IterL3FromL1MuonTrackCutClassifierNoVtx.vertices = "hltTrimmedPixelVertices"
	process.hltIter0IterL3FromL1MuonTrackCutClassifierNoVtx.mva.minPixelHits = [0, 0, 0]
	process.hltIter0IterL3FromL1MuonTrackCutClassifierNoVtx.mva.min3DLayers = [0, 0, 0 ]


	process.hltIterL3MuonMergedNoVtx.selectedTrackQuals = ['hltIterL3OIMuonTrackSelectionHighPurityNoVtx','hltIter0IterL3MuonTrackSelectionHighPurityNoVtx']
	process.hltIterL3MuonMergedNoVtx.TrackProducers = ['hltIterL3OIMuonTrackSelectionHighPurityNoVtx','hltIter0IterL3MuonTrackSelectionHighPurityNoVtx']

	process.hltIterL3MuonAndMuonFromL1MergedNoVtx.selectedTrackQuals = ['hltIterL3MuonMergedNoVtx','hltIter0IterL3FromL1MuonTrackSelectionHighPurityNoVtx']
	process.hltIterL3MuonAndMuonFromL1MergedNoVtx.TrackProducers = ['hltIterL3MuonMergedNoVtx','hltIter0IterL3FromL1MuonTrackSelectionHighPurityNoVtx']

	process.hltL3MuonsIterL3LinksNoVtx.InclusiveTrackerTrackCollection = "hltIterL3MuonAndMuonFromL1MergedNoVtx"

	process.hltIterL3MuonsNoVtx.TrackExtractorPSet.inputTrackCollection = "hltIter0IterL3FromL1MuonTrackSelectionHighPurityNoVtx"
	process.hltIterL3MuonsNoVtx.inputCollectionLabels = ['hltIterL3MuonAndMuonFromL1MergedNoVtx','hltL3MuonsIterL3LinksNoVtx']

	# the tracker isolatin part
	if hasattr(process, "HLTIterativeTrackingL3MuonIteration0NoVtx"):
		process.hltPixelTracksTrackingRegionsForSeedsL3MuonNoVtx.RegionPSet.ptMin = 0.3
		process.hltPixelTracksTrackingRegionsForSeedsL3MuonNoVtx.RegionPSet.vertexCollection = "hltPixelVertices"

		process.hltPixelTracksInRegionIter0L3MuonNoVtx = cms.EDProducer("TrackSelectorByRegion",
			  produceTrackCollection = cms.bool(True),
			  produceMask = cms.bool(False),
			  tracks = cms.InputTag("hltPixelTracks"),
			  regions = cms.InputTag("hltPixelTracksTrackingRegionsForSeedsL3MuonNoVtx")

			)
		process.hltIter0L3MuonPixelSeedsFromPixelTracksNoVtx.InputCollection = "hltPixelTracksInRegionIter0L3MuonNoVtx"
		process.hltIter0L3MuonPixelSeedsFromPixelTracksNoVtx.InputVertexCollection = "hltPixelVertices"
		process.hltIter0L3MuonTrackCutClassifierNoVtx.vertices = "hltPixelVertices"

		process.HLTIterativeTrackingL3MuonIteration0NoVtx = cms.Sequence( process.hltPixelTracksTrackingRegionsForSeedsL3MuonNoVtx + process.hltPixelTracksInRegionIter0L3MuonNoVtx + process.hltIter0L3MuonPixelSeedsFromPixelTracksNoVtx + process.hltIter0L3MuonCkfTrackCandidatesNoVtx + process.hltIter0L3MuonCtfWithMaterialTracksNoVtx + process.hltIter0L3MuonTrackCutClassifierNoVtx + process.hltIter0L3MuonTrackSelectionHighPurityNoVtx )

		if hasattr(process, "HLTTrackReconstructionForIsoL3MuonIter02NoVtx"):
			process.HLTTrackReconstructionForIsoL3MuonIter02NoVtx = cms.Sequence( process.HLTDoLocalPixelSequence + process.HLTDoLocalStripSequence + process.HLTIterativeTrackingL3MuonIteration0NoVtx )
			if hasattr(process, "hltMuonTkRelIsolationCut0p09MapNoVtx"):
				process.hltMuonTkRelIsolationCut0p09MapNoVtx.TrkExtractorPSet.inputTrackCollection = "hltIter0L3MuonTrackSelectionHighPurityNoVtx"

	return process


def customizeMuonHLTForPatatrackOpenMu(process, loadPatatrack=False, newProcessName = "MYHLT"):
	if not hasattr(process, "HLTL3muonrecoNocandOpenMuSequence"):
		return process

	if loadPatatrack:
    	# -- modify process to create patatrack pixel tracks and vertices
		from HLTrigger.Configuration.customizeHLTforPatatrack import customizeHLTforPatatrackTriplets


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
	 
		process = customizeHLTforPatatrackTriplets(process)    

	process.hltPixelTracksInRegionL2OpenMu = cms.EDProducer("TrackSelectorByRegion",
	  produceTrackCollection = cms.bool(True),
	  produceMask = cms.bool(False),
	  tracks = cms.InputTag("hltPixelTracks"),
	  regions = cms.InputTag("hltIterL3MuonPixelTracksTrackingRegionsOpenMu")

	)

	process.hltIterL3MuonPixelTracksTrackingRegionsOpenMu.Pt_min = 0.0


	process.HLTIterL3MuonRecoPixelTracksOpenMuSequence = cms.Sequence( process.HLTRecopixelvertexingSequence + process.hltIterL3MuonPixelTracksTrackingRegionsOpenMu + process.hltPixelTracksInRegionL2OpenMu )

	process.hltIter0IterL3MuonPixelSeedsFromPixelTracksOpenMu.InputCollection = "hltPixelTracksInRegionL2OpenMu"
	process.hltIter0IterL3MuonPixelSeedsFromPixelTracksOpenMu.includeFourthHit = True
	process.hltIter0IterL3MuonPixelSeedsFromPixelTracksOpenMu.InputVertexCollection = ""

	process.hltL3MuonsIterL3IOOpenMu.L3TrajBuilderParameters.tkTrajLabel = "hltIter0IterL3MuonTrackSelectionHighPurityOpenMu"
	process.hltL3MuonsIterL3IOOpenMu.L3TrajBuilderParameters.tkTrajVertex = "hltTrimmedPixelVertices"

	process.HLTIterativeTrackingIteration0ForIterL3MuonOpenMu = cms.Sequence( process.hltIter0IterL3MuonPixelSeedsFromPixelTracksOpenMu + process.hltIter0IterL3MuonCkfTrackCandidatesOpenMu + process.hltIter0IterL3MuonCtfWithMaterialTracksOpenMu + process.hltIter0IterL3MuonTrackCutClassifierOpenMu + process.hltIter0IterL3MuonTrackSelectionHighPurityOpenMu)

	process.HLTIterL3IOmuonTkCandidateOpenMuSequence = cms.Sequence( process.HLTIterL3MuonRecoPixelTracksOpenMuSequence + process.HLTIterativeTrackingIteration0ForIterL3MuonOpenMu + process.hltL3MuonsIterL3IOOpenMu )

	process.hltIter0IterL3MuonTrackCutClassifierOpenMu.vertices = "hltTrimmedPixelVertices"
	process.hltIter0IterL3MuonTrackCutClassifierOpenMu.mva.minPixelHits = [0, 0, 0]
	process.hltIter0IterL3MuonTrackCutClassifierOpenMu.mva.min3DLayers = [0, 0, 0]


	process.hltPixelTracksInRegionL1OpenMu = cms.EDProducer("TrackSelectorByRegion",
	  produceTrackCollection = cms.bool(True),
	  produceMask = cms.bool(False),
	  tracks = cms.InputTag("hltPixelTracks"),
	  regions = cms.InputTag("hltIterL3FromL1MuonPixelTracksTrackingRegionsOpenMu")

	)

	process.hltIterL3FromL1MuonPixelTracksTrackingRegionsOpenMu.RegionPSet.ptMin = 0.0
	process.hltIterL3FromL1MuonPixelTracksTrackingRegionsOpenMu.RegionPSet.maxNRegions = 5

	process.HLTRecopixelvertexingSequenceForIterL3FromL1MuonOpenMu = cms.Sequence( process.HLTRecopixelvertexingSequence + process.hltIterL3FromL1MuonPixelTracksTrackingRegionsOpenMu + process.hltPixelTracksInRegionL1OpenMu )

	process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksOpenMu.InputCollection = "hltPixelTracksInRegionL1OpenMu"
	process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksOpenMu.InputVertexCollection = ""
	process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksOpenMu.includeFourthHit = True


	process.HLTIterativeTrackingIteration0ForIterL3FromL1MuonOpenMu = cms.Sequence( process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksOpenMu + process.hltIter0IterL3FromL1MuonCkfTrackCandidatesOpenMu + process.hltIter0IterL3FromL1MuonCtfWithMaterialTracksOpenMu + process.hltIter0IterL3FromL1MuonTrackCutClassifierOpenMu + process.hltIter0IterL3FromL1MuonTrackSelectionHighPurityOpenMu )

	process.HLTIterL3IOmuonFromL1TkCandidateOpenMuSequence = cms.Sequence( process.HLTRecopixelvertexingSequenceForIterL3FromL1MuonOpenMu + process.HLTIterativeTrackingIteration0ForIterL3FromL1MuonOpenMu )

	process.hltIter0IterL3FromL1MuonTrackCutClassifierOpenMu.vertices = "hltTrimmedPixelVertices"
	process.hltIter0IterL3FromL1MuonTrackCutClassifierOpenMu.mva.minPixelHits = [0, 0, 0]
	process.hltIter0IterL3FromL1MuonTrackCutClassifierOpenMu.mva.min3DLayers = [0, 0, 0]


	process.hltIterL3MuonMergedOpenMu.selectedTrackQuals = ['hltIterL3OIMuonTrackSelectionHighPurityOpenMu','hltIter0IterL3MuonTrackSelectionHighPurityOpenMu']
	process.hltIterL3MuonMergedOpenMu.TrackProducers = ['hltIterL3OIMuonTrackSelectionHighPurityOpenMu','hltIter0IterL3MuonTrackSelectionHighPurityOpenMu']

	process.hltIterL3MuonAndMuonFromL1MergedOpenMu.selectedTrackQuals = ['hltIterL3MuonMergedOpenMu','hltIter0IterL3FromL1MuonTrackSelectionHighPurityOpenMu']
	process.hltIterL3MuonAndMuonFromL1MergedOpenMu.TrackProducers = ['hltIterL3MuonMergedOpenMu','hltIter0IterL3FromL1MuonTrackSelectionHighPurityOpenMu']

	process.hltL3MuonsIterL3LinksOpenMu.InclusiveTrackerTrackCollection = "hltIterL3MuonAndMuonFromL1MergedOpenMu"

	process.hltIterL3MuonsOpenMu.TrackExtractorPSet.inputTrackCollection = "hltIter0IterL3FromL1MuonTrackSelectionHighPurityOpenMu"
	process.hltIterL3MuonsOpenMu.inputCollectionLabels = ['hltIterL3MuonAndMuonFromL1MergedOpenMu','hltL3MuonsIterL3LinksOpenMu']

	
	return process


def customizerFuncForMuonHLTSeeding(
    process, newProcessName = "MYHLT",
    doSort = False,
    nSeedsMaxBs = (99999, 99999), nSeedsMaxEs = (99999, 99999),
    mvaCutBs = (0.01, 0.01), mvaCutEs = (0.01, 0.01)):

    if not hasattr(process, "HLTIterativeTrackingIteration2ForIterL3Muon") or\
       not hasattr(process, "HLTIterativeTrackingIteration2ForIterL3FromL1Muon"):
        return process

    import HLTrigger.Configuration.MuonHLTForRun3.mvaScale as _mvaScale

    # print "\nCustomizing Seed MVA Classifier:"
    # print "\tdoSort:      ", doSort
    # print "\tnSeedsMaxBs: ", nSeedsMaxBs
    # print "\tnSeedsMaxEs: ", nSeedsMaxEs
    # print "\tmvaCutBs:    ", mvaCutBs
    # print "\tmvaCutEs:    ", mvaCutEs

    # -- Seed MVA Classifiers
    process.hltIter2IterL3MuonPixelSeedsFiltered = cms.EDProducer("MuonHLTSeedMVAClassifier",
        rejectAll = cms.bool(False),
        isFromL1 = cms.bool(False),

        src    = cms.InputTag("hltIter2IterL3MuonPixelSeeds", "", newProcessName),
        L1Muon = cms.InputTag("hltGtStage2Digis", "Muon", newProcessName),
        L2Muon = cms.InputTag("hltL2MuonCandidates", "", newProcessName),

        mvaFileBL2 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/v7Fast_Barrel_hltIter2.xml"),
        mvaFileEL2 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/v7Fast_Endcap_hltIter2.xml"),

        mvaScaleMeanBL2 = cms.vdouble( getattr(_mvaScale, "v7Fast_Barrel_hltIter2_ScaleMean") ),
        mvaScaleStdBL2  = cms.vdouble( getattr(_mvaScale, "v7Fast_Barrel_hltIter2_ScaleStd") ),
        mvaScaleMeanEL2 = cms.vdouble( getattr(_mvaScale, "v7Fast_Endcap_hltIter2_ScaleMean") ),
        mvaScaleStdEL2  = cms.vdouble( getattr(_mvaScale, "v7Fast_Endcap_hltIter2_ScaleStd") ),

        doSort = cms.bool(doSort),
        nSeedsMaxB = cms.int32(nSeedsMaxBs[0]),
        nSeedsMaxE = cms.int32(nSeedsMaxEs[0]),

        mvaCutB = cms.double(mvaCutBs[0]),
        mvaCutE = cms.double(mvaCutEs[0])
    )
    process.hltIter2IterL3FromL1MuonPixelSeedsFiltered = cms.EDProducer("MuonHLTSeedMVAClassifier",
        rejectAll = cms.bool(False),
        isFromL1 = cms.bool(True),

        src    = cms.InputTag("hltIter2IterL3FromL1MuonPixelSeeds", "", newProcessName),
        L1Muon = cms.InputTag("hltGtStage2Digis", "Muon", newProcessName),
        L2Muon = cms.InputTag("hltL2MuonCandidates", "", newProcessName),

        mvaFileBL1 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/v7Fast_Barrel_hltIter2FromL1.xml"),
        mvaFileEL1 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/v7Fast_Endcap_hltIter2FromL1.xml"),

        mvaScaleMeanBL1 = cms.vdouble( getattr(_mvaScale, "v7Fast_Barrel_hltIter2FromL1_ScaleMean") ),
        mvaScaleStdBL1  = cms.vdouble( getattr(_mvaScale, "v7Fast_Barrel_hltIter2FromL1_ScaleStd") ),
        mvaScaleMeanEL1 = cms.vdouble( getattr(_mvaScale, "v7Fast_Endcap_hltIter2FromL1_ScaleMean") ),
        mvaScaleStdEL1  = cms.vdouble( getattr(_mvaScale, "v7Fast_Endcap_hltIter2FromL1_ScaleStd") ),

        doSort = cms.bool(doSort),
        nSeedsMaxB = cms.int32(nSeedsMaxBs[1]),
        nSeedsMaxE = cms.int32(nSeedsMaxEs[1]),

        mvaCutB = cms.double(mvaCutBs[1]),
        mvaCutE = cms.double(mvaCutEs[1])
    )

    # -- Track Candidates
    process.hltIter2IterL3MuonCkfTrackCandidates.src       = cms.InputTag("hltIter2IterL3MuonPixelSeedsFiltered", "", newProcessName)
    process.hltIter2IterL3FromL1MuonCkfTrackCandidates.src = cms.InputTag("hltIter2IterL3FromL1MuonPixelSeedsFiltered", "", newProcessName)

    # -- Sequences
    process.HLTIterativeTrackingIteration2ForIterL3Muon = cms.Sequence(
        process.hltIter2IterL3MuonClustersRefRemoval+
        process.hltIter2IterL3MuonMaskedMeasurementTrackerEvent+
        process.hltIter2IterL3MuonPixelLayerTriplets+
        process.hltIter2IterL3MuonPixelClusterCheck+
        process.hltIter2IterL3MuonPixelHitDoublets+
        process.hltIter2IterL3MuonPixelHitTriplets+
        process.hltIter2IterL3MuonPixelSeeds+
        process.hltIter2IterL3MuonPixelSeedsFiltered+
        process.hltIter2IterL3MuonCkfTrackCandidates+
        process.hltIter2IterL3MuonCtfWithMaterialTracks+
        process.hltIter2IterL3MuonTrackCutClassifier+
        process.hltIter2IterL3MuonTrackSelectionHighPurity
    )
    process.HLTIterativeTrackingIteration2ForIterL3FromL1Muon = cms.Sequence(
        process.hltIter2IterL3FromL1MuonClustersRefRemoval+
        process.hltIter2IterL3FromL1MuonMaskedMeasurementTrackerEvent+
        process.hltIter2IterL3FromL1MuonPixelLayerTriplets+
        process.hltIter2IterL3FromL1MuonPixelClusterCheck+
        process.hltIter2IterL3FromL1MuonPixelHitDoublets+
        process.hltIter2IterL3FromL1MuonPixelHitTriplets+
        process.hltIter2IterL3FromL1MuonPixelSeeds+
        process.hltIter2IterL3FromL1MuonPixelSeedsFiltered+
        process.hltIter2IterL3FromL1MuonCkfTrackCandidates+
        process.hltIter2IterL3FromL1MuonCtfWithMaterialTracks+
        process.hltIter2IterL3FromL1MuonTrackCutClassifier+
        process.hltIter2IterL3FromL1MuonTrackSelectionHighPurity
    )

    return process


def customizeIOSeedingPatatrack(
	process, newProcessName = "MYHLT",
	doSort = False,
	nSeedsMaxBs = (99999, 99999), nSeedsMaxEs = (99999, 99999),
	mvaCutBs = (0.01, 0.01), mvaCutEs = (0.01, 0.01)):

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

		mvaFileBL1 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/xgb_Run3_Iter0FromL1_PatatrackSeeds_barrel_v2.xml"),
		mvaFileEL1 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/xgb_Run3_Iter0FromL1_PatatrackSeeds_endcap_v2.xml"),

		mvaScaleMeanBL1 = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0FromL1_PatatrackSeeds_barrel_v2_ScaleMean") ),
		mvaScaleStdBL1  = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0FromL1_PatatrackSeeds_barrel_v2_ScaleStd") ),
		mvaScaleMeanEL1 = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0FromL1_PatatrackSeeds_endcap_v2_ScaleMean") ),
		mvaScaleStdEL1  = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0FromL1_PatatrackSeeds_endcap_v2_ScaleStd") ),

		mvaFileBL2 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/xgb_Run3_Iter0_PatatrackSeeds_barrel_v2.xml"),
		mvaFileEL2 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/xgb_Run3_Iter0_PatatrackSeeds_endcap_v2.xml"),

		mvaScaleMeanBL2 = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0_PatatrackSeeds_barrel_v2_ScaleMean") ),
		mvaScaleStdBL2  = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0_PatatrackSeeds_barrel_v2_ScaleStd") ),
		mvaScaleMeanEL2 = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0_PatatrackSeeds_endcap_v2_ScaleMean") ),
		mvaScaleStdEL2  = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0_PatatrackSeeds_endcap_v2_ScaleStd") ),

		doSort = cms.bool(doSort),
		nSeedsMaxB = cms.int32(nSeedsMaxBs[0]),
		nSeedsMaxE = cms.int32(nSeedsMaxEs[0]),

		mvaCutB = cms.double(mvaCutBs[0]),
		mvaCutE = cms.double(mvaCutEs[0])
	)
	process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksFiltered = cms.EDProducer("MuonHLTSeedMVAClassifier",
		rejectAll = cms.bool(False),
		isFromL1 = cms.bool(True),

		src    = cms.InputTag("hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks"),
		L1Muon = cms.InputTag("hltGtStage2Digis", "Muon"),
		L2Muon = cms.InputTag("hltL2MuonCandidates", ""),

		mvaFileBL1 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/xgb_Run3_Iter0FromL1_PatatrackSeeds_barrel_v2.xml"),
		mvaFileEL1 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/xgb_Run3_Iter0FromL1_PatatrackSeeds_endcap_v2.xml"),

		mvaScaleMeanBL1 = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0FromL1_PatatrackSeeds_barrel_v2_ScaleMean") ),
		mvaScaleStdBL1  = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0FromL1_PatatrackSeeds_barrel_v2_ScaleStd") ),
		mvaScaleMeanEL1 = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0FromL1_PatatrackSeeds_endcap_v2_ScaleMean") ),
		mvaScaleStdEL1  = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0FromL1_PatatrackSeeds_endcap_v2_ScaleStd") ),

		mvaFileBL2 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/xgb_Run3_Iter0_PatatrackSeeds_barrel_v2.xml"),
		mvaFileEL2 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/xgb_Run3_Iter0_PatatrackSeeds_endcap_v2.xml"),

		mvaScaleMeanBL2 = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0_PatatrackSeeds_barrel_v2_ScaleMean") ),
		mvaScaleStdBL2  = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0_PatatrackSeeds_barrel_v2_ScaleStd") ),
		mvaScaleMeanEL2 = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0_PatatrackSeeds_endcap_v2_ScaleMean") ),
		mvaScaleStdEL2  = cms.vdouble( getattr(_mvaScale, "xgb_Run3_Iter0_PatatrackSeeds_endcap_v2_ScaleStd") ),

		doSort = cms.bool(doSort),
		nSeedsMaxB = cms.int32(nSeedsMaxBs[1]),
		nSeedsMaxE = cms.int32(nSeedsMaxEs[1]),

		mvaCutB = cms.double(mvaCutBs[1]),
		mvaCutE = cms.double(mvaCutEs[1])
	)

	# -- Track Candidates
	process.hltIter0IterL3MuonCkfTrackCandidates.src       = "hltIter0IterL3MuonPixelSeedsFromPixelTracksFiltered"
	process.hltIter0IterL3FromL1MuonCkfTrackCandidates.src = "hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksFiltered"

	# -- Sequences
	process.HLTIterativeTrackingIteration0ForIterL3Muon = cms.Sequence(
		process.hltIter0IterL3MuonPixelSeedsFromPixelTracks +
		process.hltIter0IterL3MuonPixelSeedsFromPixelTracksFiltered +
		process.hltIter0IterL3MuonCkfTrackCandidates +
		process.hltIter0IterL3MuonCtfWithMaterialTracks +
		process.hltIter0IterL3MuonTrackCutClassifier +
		process.hltIter0IterL3MuonTrackSelectionHighPurity
	)
	process.HLTIterativeTrackingIteration0ForIterL3FromL1Muon = cms.Sequence(
		process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks +
		process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksFiltered +
		process.hltIter0IterL3FromL1MuonCkfTrackCandidates +
		process.hltIter0IterL3FromL1MuonCtfWithMaterialTracks +
		process.hltIter0IterL3FromL1MuonTrackCutClassifier +
		process.hltIter0IterL3FromL1MuonTrackSelectionHighPurity 
	)

	return process


def customizeRhoProducersForIso(process):
    if hasattr(process, "hltFixedGridRhoFastjetECALMFForMuons"):
        delattr(process, "hltFixedGridRhoFastjetECALMFForMuons")

        process.hltFixedGridRhoFastjetECALMFForMuons = cms.EDProducer( "FixedGridRhoProducerFastjetFromRecHit",
            hbheRecHitsTag = cms.InputTag( "hltHbhereco" ),
            ebRecHitsTag = cms.InputTag( 'hltEcalRecHit','EcalRecHitsEB' ),
            eeRecHitsTag = cms.InputTag( 'hltEcalRecHit','EcalRecHitsEE' ),
            eThresHB = cms.vdouble(0.1, 0.2, 0.3, 0.3),
            eThresHE = cms.vdouble(0.1, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2),
            maxRapidity = cms.double( 2.5 ),
            gridSpacing = cms.double( 0.55 ),
            skipHCAL = cms.bool(True), # -- skip HCAL
            skipECAL = cms.bool(False)
        )

    if hasattr(process, "hltFixedGridRhoFastjetHCAL"):
        delattr(process, "hltFixedGridRhoFastjetHCAL")

        process.hltFixedGridRhoFastjetHCAL = cms.EDProducer( "FixedGridRhoProducerFastjetFromRecHit",
            hbheRecHitsTag = cms.InputTag( "hltHbhereco" ),
            ebRecHitsTag = cms.InputTag( 'hltEcalRecHit','EcalRecHitsEB' ),
            eeRecHitsTag = cms.InputTag( 'hltEcalRecHit','EcalRecHitsEE' ),
            eThresHB = cms.vdouble(0.1, 0.2, 0.3, 0.3),
            eThresHE = cms.vdouble(0.1, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2),
            maxRapidity = cms.double( 2.5 ),
            gridSpacing = cms.double( 0.55 ),
            skipHCAL = cms.bool(False),
            skipECAL = cms.bool(True) # -- skip ECAL
        )

    if hasattr(process, "HLTL3muonEcalPFisorecoSequenceNoBoolsForMuons"):
        process.HLTL3muonEcalPFisorecoSequenceNoBoolsForMuons = cms.Sequence( 
            process.HLTDoFullUnpackingEgammaEcalMFSequence + 
            process.HLTDoLocalHcalSequence + 
            process.hltFixedGridRhoFastjetECALMFForMuons + 
            process.hltFixedGridRhoFastjetHCAL + 
            process.HLTPFClusteringEcalMFForMuons + 
            process.hltMuonEcalMFPFClusterIsoForMuons
        )

    return process


def customizeTrkIsoFullHLTTracking(process):
    # TRK_newTracking must be loaded in advance
    if hasattr(process, "HLTTrackReconstructionForIsoL3MuonIter02"):
        process.HLTTrackReconstructionForIsoL3MuonIter02 = cms.Sequence(
            process.HLTDoLocalPixelSequence +
            process.HLTDoLocalStripSequence +
            process.HLTIterativeTrackingIter02
        )
        if hasattr(process, "hltMuonTkRelIsolationCut0p07Map"):
            process.hltMuonTkRelIsolationCut0p07Map.TrkExtractorPSet.inputTrackCollection = cms.InputTag("hltMergedTracks")
        if hasattr(process, "hltL3MuonCombRelIsolationVVVL"):
            process.hltL3MuonCombRelIsolationVVVL.TrkExtractorPSet.inputTrackCollection = cms.InputTag("hltMergedTracks")

    if hasattr(process, "HLTL3muontrkisorecoSequence"):
        process.HLTL3muontrkisorecoSequence = cms.Sequence(
            process.HLTDoLocalPixelSequence +
            process.HLTDoLocalStripSequence +
            process.HLTIterativeTrackingIter02
        )
        if hasattr(process, "hltL3MuonRelTrkIsolationVVL"):
            process.hltL3MuonRelTrkIsolationVVL.TrkExtractorPSet.inputTrackCollection = cms.InputTag("hltMergedTracks")
        if hasattr(process, "hltTauPt15MuPts711Mass1p3to2p1IsoCharge1"):
            process.hltTauPt15MuPts711Mass1p3to2p1IsoCharge1.IsoTracksSrc = cms.InputTag("hltMergedTracks")
        if hasattr(process, "hltTauPt15MuPts711Mass1p3to2p1Iso"):
            process.hltTauPt15MuPts711Mass1p3to2p1Iso.IsoTracksSrc = cms.InputTag("hltMergedTracks")

    return process


def customizeTrkIso(process, nRegionsFactor = 1, isoWPs = []):  # [0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10]
    # override tracking parameters...
    process.hltIter0L3MuonPixelSeedsFromPixelTracks = cms.EDProducer("SeedGeneratorFromProtoTracksEDProducer",
        InputCollection = cms.InputTag("hltPixelTracksInRegionIter0L3Muon"),
        InputVertexCollection = cms.InputTag( "hltTrimmedPixelVertices" ),
        originHalfLength = cms.double( 0.3 ),
        originRadius = cms.double( 0.1 ),
        useProtoTrackKinematics = cms.bool( False ),
        useEventsWithNoVertex = cms.bool( True ),
        TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
        usePV = cms.bool( False ),
        includeFourthHit = cms.bool( True ),
        SeedCreatorPSet = cms.PSet(  refToPSet_ = cms.string( "HLTSeedFromProtoTracks" ) )
    )

    process.hltIter0L3MuonCkfTrackCandidates = cms.EDProducer("CkfTrackCandidateMaker",
        cleanTrajectoryAfterInOut = cms.bool( False ),
        doSeedingRegionRebuilding = cms.bool( False ),
        onlyPixelHitsForSeedCleaner = cms.bool( False ),
        reverseTrajectories = cms.bool( False ),
        useHitsSplitting = cms.bool( False ),
        MeasurementTrackerEvent = cms.InputTag( "hltSiStripClusters" ),
        src = cms.InputTag( "hltIter0L3MuonPixelSeedsFromPixelTracks" ),
        clustersToSkip = cms.InputTag( "" ),
        phase2clustersToSkip = cms.InputTag( "" ),
        TrajectoryBuilderPSet = cms.PSet(  refToPSet_ = cms.string( "HLTIter0GroupedCkfTrajectoryBuilderIT" ) ),
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

    process.hltIter0L3MuonCtfWithMaterialTracks = cms.EDProducer("TrackProducer",
        useSimpleMF = cms.bool( True ),
        SimpleMagneticField = cms.string( "ParabolicMf" ),
        src = cms.InputTag( "hltIter0L3MuonCkfTrackCandidates" ),
        clusterRemovalInfo = cms.InputTag( "" ),
        beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
        Fitter = cms.string( "hltESPFittingSmootherIT" ),
        useHitsSplitting = cms.bool( False ),
        alias = cms.untracked.string( "ctfWithMaterialTracks" ),
        TrajectoryInEvent = cms.bool( False ),
        TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
        AlgorithmName = cms.string( "hltIter0" ),
        Propagator = cms.string( "hltESPRungeKuttaTrackerPropagator" ),
        GeometricInnerState = cms.bool( True ),
        NavigationSchool = cms.string( "" ),
        MeasurementTracker = cms.string( "" ),
        MeasurementTrackerEvent = cms.InputTag( "hltSiStripClusters" )
    )

    process.hltIter0L3MuonTrackCutClassifier = cms.EDProducer("TrackCutClassifier",
        src = cms.InputTag( "hltIter0L3MuonCtfWithMaterialTracks" ),
        beamspot = cms.InputTag( "hltOnlineBeamSpot" ),
        vertices = cms.InputTag( "hltTrimmedPixelVertices" ),
        ignoreVertices = cms.bool( False ),
        qualityCuts = cms.vdouble( -0.7, 0.1, 0.7 ),
        mva = cms.PSet( 
          minPixelHits = cms.vint32( 0, 0, 0 ),
          maxDzWrtBS = cms.vdouble( 3.40282346639E38, 24.0, 15.0 ),
          dr_par = cms.PSet( 
            d0err = cms.vdouble( 0.003, 0.003, 0.003 ),
            dr_par2 = cms.vdouble( 3.40282346639E38, 0.6, 0.6 ),
            dr_par1 = cms.vdouble( 3.40282346639E38, 0.8, 0.8 ),
            dr_exp = cms.vint32( 4, 4, 4 ),
            d0err_par = cms.vdouble( 0.001, 0.001, 0.001 )
          ),
          maxLostLayers = cms.vint32( 1, 1, 1 ),
          min3DLayers = cms.vint32( 0, 0, 0 ),
          dz_par = cms.PSet( 
            dz_par1 = cms.vdouble( 3.40282346639E38, 0.75, 0.75 ),
            dz_par2 = cms.vdouble( 3.40282346639E38, 0.5, 0.5 ),
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

    process.hltIter0L3MuonTrackSelectionHighPurity = cms.EDProducer("TrackCollectionFilterCloner",
        copyExtras = cms.untracked.bool(True),
        copyTrajectories = cms.untracked.bool(False),
        minQuality = cms.string('highPurity'),
        originalMVAVals = cms.InputTag("hltIter0L3MuonTrackCutClassifier","MVAValues"),
        originalQualVals = cms.InputTag("hltIter0L3MuonTrackCutClassifier","QualityMasks"),
        originalSource = cms.InputTag("hltIter0L3MuonCtfWithMaterialTracks")
    )

    # update ROIs
    process.hltPixelTracksTrackingRegionsForSeedsL3Muon.RegionPSet.maxNVertices = cms.int32( 1 * nRegionsFactor )
    process.hltPixelTracksTrackingRegionsForSeedsL3Muon.RegionPSet.maxNRegions  = cms.int32( 10 * nRegionsFactor )

    # scan tracker iso WPs
    if len(isoWPs) > 0:
        # IMPORTANT: only works without prescale
        process.HLT_IsoMu24_base = cms.Sequence(
            process.HLTBeginSequence+
            process.hltL1sSingleMu22+
            process.hltPreIsoMu24+
            process.hltL1fL1sMu22L1Filtered0+
            process.HLTL2muonrecoSequence+
            cms.ignore(process.hltL2fL1sSingleMu22L1f0L2Filtered10Q)+
            process.HLTL3muonrecoSequence+
            cms.ignore(process.hltL1fForIterL3L1fL1sMu22L1Filtered0)+
            process.hltL3fL1sSingleMu22L1f0L2f10QL3Filtered24Q+

            # process.HLTMu24IsolationSequence+
            process.HLTL3muonEcalPFisorecoSequenceNoBoolsForMuons+
            process.hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3pfecalIsoRhoFilteredEB0p14EE0p10+
            process.HLTL3muonHcalPFisorecoSequenceNoBoolsForMuons+
            process.hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3pfhcalIsoRhoFilteredHB0p16HE0p20+
            process.HLTTrackReconstructionForIsoL3MuonIter02

            # process.hltMuonTkRelIsolationCut0p07Map+
            # process.hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07+

            # process.HLTEndSequence
        )

        for cut in isoWPs:
            mod = process.hltMuonTkRelIsolationCut0p07Map.clone()
            mod.CutsPSet.Thresholds = cms.vdouble(cut)
            modname = "hltMuonTkRelIsolationCut%.2fMapTmp" % cut
            modname = modname.replace(".", "p")
            setattr(process,modname,mod)

            filt = process.hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07.clone()
            filt.DepTag = cms.VInputTag(modname)
            filtname = "hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered%.2fTmp" % cut
            filtname = filtname.replace(".", "p")
            setattr(process,filtname,filt)

            path = cms.Path(process.HLT_IsoMu24_base)
            path.insert(1, getattr(process, modname))
            path.insert(2, getattr(process, filtname))
            path.insert(3, process.HLTEndSequence)
            pathname = "HLT_IsoMu24_trkIso%.2f_vTmp" % cut
            pathname = pathname.replace(".", "p")
            setattr(process,pathname,path)

            process.schedule.extend([getattr(process, pathname)])

    return process


def customizeTrkIsoNoVtx(process, nRegionsFactor = 1):  # [0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10]
    # override tracking parameters...
    process.hltIter0L3MuonPixelSeedsFromPixelTracksNoVtx = cms.EDProducer("SeedGeneratorFromProtoTracksEDProducer",
        InputCollection = cms.InputTag("hltPixelTracksInRegionIter0L3MuonNoVtx"),
        InputVertexCollection = cms.InputTag( "hltTrimmedPixelVertices" ),
        originHalfLength = cms.double( 0.3 ),
        originRadius = cms.double( 0.1 ),
        useProtoTrackKinematics = cms.bool( False ),
        useEventsWithNoVertex = cms.bool( True ),
        TTRHBuilder = cms.string( "hltESPTTRHBuilderPixelOnly" ),
        usePV = cms.bool( False ),
        includeFourthHit = cms.bool( True ),
        SeedCreatorPSet = cms.PSet(  refToPSet_ = cms.string( "HLTSeedFromProtoTracks" ) )
    )

    process.hltIter0L3MuonCkfTrackCandidatesNoVtx = cms.EDProducer("CkfTrackCandidateMaker",
        cleanTrajectoryAfterInOut = cms.bool( False ),
        doSeedingRegionRebuilding = cms.bool( False ),
        onlyPixelHitsForSeedCleaner = cms.bool( False ),
        reverseTrajectories = cms.bool( False ),
        useHitsSplitting = cms.bool( False ),
        MeasurementTrackerEvent = cms.InputTag( "hltSiStripClusters" ),
        src = cms.InputTag( "hltIter0L3MuonPixelSeedsFromPixelTracksNoVtx" ),
        clustersToSkip = cms.InputTag( "" ),
        phase2clustersToSkip = cms.InputTag( "" ),
        TrajectoryBuilderPSet = cms.PSet(  refToPSet_ = cms.string( "HLTIter0GroupedCkfTrajectoryBuilderIT" ) ),
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

    process.hltIter0L3MuonCtfWithMaterialTracksNoVtx = cms.EDProducer("TrackProducer",
        useSimpleMF = cms.bool( True ),
        SimpleMagneticField = cms.string( "ParabolicMf" ),
        src = cms.InputTag( "hltIter0L3MuonCkfTrackCandidatesNoVtx" ),
        clusterRemovalInfo = cms.InputTag( "" ),
        beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
        Fitter = cms.string( "hltESPFittingSmootherIT" ),
        useHitsSplitting = cms.bool( False ),
        alias = cms.untracked.string( "ctfWithMaterialTracks" ),
        TrajectoryInEvent = cms.bool( False ),
        TTRHBuilder = cms.string( "hltESPTTRHBWithTrackAngle" ),
        AlgorithmName = cms.string( "hltIter0" ),
        Propagator = cms.string( "hltESPRungeKuttaTrackerPropagator" ),
        GeometricInnerState = cms.bool( True ),
        NavigationSchool = cms.string( "" ),
        MeasurementTracker = cms.string( "" ),
        MeasurementTrackerEvent = cms.InputTag( "hltSiStripClusters" )
    )

    process.hltIter0L3MuonTrackCutClassifierNoVtx = cms.EDProducer("TrackCutClassifier",
        src = cms.InputTag( "hltIter0L3MuonCtfWithMaterialTracksNoVtx" ),
        beamspot = cms.InputTag( "hltOnlineBeamSpot" ),
        vertices = cms.InputTag( "hltTrimmedPixelVertices" ),
        ignoreVertices = cms.bool( False ),
        qualityCuts = cms.vdouble( -0.7, 0.1, 0.7 ),
        mva = cms.PSet( 
          minPixelHits = cms.vint32( 0, 0, 0 ),
          maxDzWrtBS = cms.vdouble( 3.40282346639E38, 24.0, 15.0 ),
          dr_par = cms.PSet( 
            d0err = cms.vdouble( 0.003, 0.003, 0.003 ),
            dr_par2 = cms.vdouble( 3.40282346639E38, 0.6, 0.6 ),
            dr_par1 = cms.vdouble( 3.40282346639E38, 0.8, 0.8 ),
            dr_exp = cms.vint32( 4, 4, 4 ),
            d0err_par = cms.vdouble( 0.001, 0.001, 0.001 )
          ),
          maxLostLayers = cms.vint32( 1, 1, 1 ),
          min3DLayers = cms.vint32( 0, 0, 0 ),
          dz_par = cms.PSet( 
            dz_par1 = cms.vdouble( 3.40282346639E38, 0.75, 0.75 ),
            dz_par2 = cms.vdouble( 3.40282346639E38, 0.5, 0.5 ),
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

    process.hltIter0L3MuonTrackSelectionHighPurityNoVtx = cms.EDProducer("TrackCollectionFilterCloner",
        copyExtras = cms.untracked.bool(True),
        copyTrajectories = cms.untracked.bool(False),
        minQuality = cms.string('highPurity'),
        originalMVAVals = cms.InputTag("hltIter0L3MuonTrackCutClassifierNoVtx","MVAValues"),
        originalQualVals = cms.InputTag("hltIter0L3MuonTrackCutClassifierNoVtx","QualityMasks"),
        originalSource = cms.InputTag("hltIter0L3MuonCtfWithMaterialTracksNoVtx")
    )

    # update ROIs
    process.hltPixelTracksTrackingRegionsForSeedsL3MuonNoVtx.RegionPSet.maxNVertices = cms.int32( 1 * nRegionsFactor )
    process.hltPixelTracksTrackingRegionsForSeedsL3MuonNoVtx.RegionPSet.maxNRegions  = cms.int32( 10 * nRegionsFactor )

    return process


def customizeIOROIs(process,
                    IOROIL2FactorEta = 1.0,
                    IOROIL2FactorPhi = 5.0,
                    IOROIL1FactorEta = 1.0,
                    IOROIL1FactorPhi = 5.0):
    if hasattr(process, "hltIterL3MuonPixelTracksTrackingRegions"):
        process.hltIterL3MuonPixelTracksTrackingRegions.DeltaEta = 0.2 * IOROIL2FactorEta
        process.hltIterL3MuonPixelTracksTrackingRegions.DeltaPhi = 0.15 * IOROIL2FactorPhi

    if hasattr(process, "hltIterL3FromL1MuonPixelTracksTrackingRegions"):
        process.hltIterL3FromL1MuonPixelTracksTrackingRegions.RegionPSet.deltaEta = 0.35 * IOROIL1FactorEta
        process.hltIterL3FromL1MuonPixelTracksTrackingRegions.RegionPSet.deltaPhi = 0.2  * IOROIL1FactorPhi

    return process


def addHLTL1METTkMu50(process, doQuadruplets = True):
    if not hasattr(process, "hltL1sAllETMHFSeeds"):
        return process

    if not hasattr(process, "HLTTrackerMuonSequence"):
        return process

    # Use pixel quadruplets only
    if doQuadruplets:
        if not hasattr(process, "hltPixelTracksQuadruplets"):
            process.hltPixelTracksQuadruplets = cms.EDProducer("TrackWithVertexSelector",
                copyExtras = cms.untracked.bool(False),
                copyTrajectories = cms.untracked.bool(False),
                d0Max = cms.double(999.0),
                dzMax = cms.double(999.0),
                etaMax = cms.double(999.0),
                etaMin = cms.double(-999.0),
                nSigmaDtVertex = cms.double(0.0),
                nVertices = cms.uint32(0),
                normalizedChi2 = cms.double(999999.0),
                numberOfLostHits = cms.uint32(999),
                numberOfValidHits = cms.uint32(0),
                numberOfValidPixelHits = cms.uint32(4),
                ptErrorCut = cms.double(999999.0),
                ptMax = cms.double(999999.0),
                ptMin = cms.double(0.),
                quality = cms.string('loose'),
                rhoVtx = cms.double(999999.0),
                src = cms.InputTag("hltPixelTracks"),
                timeResosTag = cms.InputTag(""),
                timesTag = cms.InputTag(""),
                useVtx = cms.bool(False),
                vertexTag = cms.InputTag("hltTrimmedPixelVertices"),
                vtxFallback = cms.bool(False),
                zetaVtx = cms.double(999999.0),
            )

        process.hltMuTrackSeeds.InputCollection = cms.InputTag("hltPixelTracksQuadruplets")

        process.HLTTrackerMuonSequence.insert(process.HLTTrackerMuonSequence.index(process.HLTDoLocalStripSequence), process.HLTRecopixelvertexingSequence)
        process.HLTTrackerMuonSequence.insert(process.HLTTrackerMuonSequence.index(process.HLTDoLocalStripSequence), process.hltPixelTracksQuadruplets)

        if hasattr(process, "HLTTrackerMuonSequenceNoVtx"):
            process.HLTTrackerMuonSequenceNoVtx.insert(process.HLTTrackerMuonSequenceNoVtx.index(process.HLTDoLocalStripSequence), process.HLTRecopixelvertexingSequence)
            process.HLTTrackerMuonSequenceNoVtx.insert(process.HLTTrackerMuonSequenceNoVtx.index(process.HLTDoLocalStripSequence), process.hltPixelTracksQuadruplets)

    # Filters and Path
    process.hltPreL1METTkMu50 = cms.EDFilter( "HLTPrescaler",
        L1GtReadoutRecordTag = cms.InputTag( "hltGtStage2Digis" ),
        offset = cms.uint32( 0 )
    )

    process.hltTkMuFiltered50Q = cms.EDFilter( "HLTMuonTrkL1TFilter",
        maxNormalizedChi2 = cms.double( 1.0E99 ),
        saveTags = cms.bool( True ),
        maxAbsEta = cms.double( 1.0E99 ),
        previousCandTag = cms.InputTag( "" ),
        minPt = cms.double( 50.0 ),
        minN = cms.uint32( 1 ),
        inputCandCollection = cms.InputTag( "hltGlbTrkMuonCands" ),
        minMuonStations = cms.int32( -1 ),
        trkMuonId = cms.uint32( 0 ),
        requiredTypeMask = cms.uint32( 0 ),
        minMuonHits = cms.int32( -1 ),
        minTrkHits = cms.int32( -1 ),
        inputMuonCollection = cms.InputTag( "hltGlbTrkMuons" ),
        allowedTypeMask = cms.uint32( 255 )
    )

    process.HLT_L1MET_TkMu50_v1 = cms.Path(
        process.HLTBeginSequence +
        process.hltL1sAllETMHFSeeds +
        process.hltPreL1METTkMu50 +
        process.HLTL2muonrecoSequence +
        process.HLTTrackerMuonSequence +
        process.hltTkMuFiltered50Q +
        process.HLTEndSequence
    )

    # TkMu + ID
    process.hltGlbTrkMuonsID = cms.EDProducer("MuonIDFilterProducerForHLT",
        allowedTypeMask = cms.uint32(0),
        applyTriggerIdLoose = cms.bool(True),
        inputMuonCollection = cms.InputTag("hltGlbTrkMuons"),
        maxNormalizedChi2 = cms.double(9999.0),
        minNMuonHits = cms.int32(0),
        minNMuonStations = cms.int32(0),
        minNTrkLayers = cms.int32(0),
        minPixHits = cms.int32(0),
        minPixLayer = cms.int32(0),
        minPt = cms.double(0.0),
        minTrkHits = cms.int32(0),
        requiredTypeMask = cms.uint32(0),
        typeMuon = cms.uint32(0)
    )

    process.hltGlbTrkMuonIDCands = cms.EDProducer("L3MuonCandidateProducerFromMuons",
        InputObjects = cms.InputTag("hltGlbTrkMuonsID")
    )

    process.hltPreL1METTkMuID50 = cms.EDFilter( "HLTPrescaler",
        L1GtReadoutRecordTag = cms.InputTag( "hltGtStage2Digis" ),
        offset = cms.uint32( 0 )
    )

    process.hltTkMuIDFiltered50Q = cms.EDFilter( "HLTMuonTrkL1TFilter",
        maxNormalizedChi2 = cms.double( 1.0E99 ),
        saveTags = cms.bool( True ),
        maxAbsEta = cms.double( 1.0E99 ),
        previousCandTag = cms.InputTag( "" ),
        minPt = cms.double( 50.0 ),
        minN = cms.uint32( 1 ),
        inputCandCollection = cms.InputTag( "hltGlbTrkMuonIDCands" ),
        minMuonStations = cms.int32( -1 ),
        trkMuonId = cms.uint32( 0 ),
        requiredTypeMask = cms.uint32( 0 ),
        minMuonHits = cms.int32( -1 ),
        minTrkHits = cms.int32( -1 ),
        inputMuonCollection = cms.InputTag( "hltGlbTrkMuonsID" ),
        allowedTypeMask = cms.uint32( 255 )
    )

    process.HLTTrackerMuonIDSequence = cms.Sequence(
        process.HLTTrackerMuonSequence +
        process.hltGlbTrkMuonsID +
        process.hltGlbTrkMuonIDCands
    )

    process.HLT_L1MET_TkMu50_ID_v1 = cms.Path(
        process.HLTBeginSequence +
        process.hltL1sAllETMHFSeeds +
        process.hltPreL1METTkMuID50 +
        process.HLTL2muonrecoSequence +
        process.HLTTrackerMuonIDSequence +
        process.hltTkMuIDFiltered50Q +
        process.HLTEndSequence
    )

    process.schedule.extend([process.HLT_L1MET_TkMu50_ID_v1])
    # process.schedule.extend([process.HLT_L1MET_TkMu50_v1, process.HLT_L1MET_TkMu50_ID_v1])

    return process


def customizeMuonHLTForAll(process, newProcessName = "MYHLT",
                           doDoubletRemoval = True,
                           doGEM = True,
                           doPatatrack = True,
                           doOISeeding = True,
                           doIOSeeding = True):
	process = customizeMuonHLTForCscSegment(process, newProcessName = newProcessName)

	if doDoubletRemoval:
		process = customizeMuonHLTForDoubletRemoval(process, newProcessName = newProcessName)

	if doGEM:
		process = customizeMuonHLTForGEM(process, newProcessName = newProcessName)

	if doPatatrack:
		process = customizeMuonHLTForPatatrackWithIsoAndTriplets(process, newProcessName = newProcessName)

	if doOISeeding:
		from RecoMuon.TrackerSeedGenerator.customizeOIseeding import customizeOIseeding
		process = customizeOIseeding(process)

	if doIOSeeding:
		process = customizeIOSeedingPatatrack(process, newProcessName = newProcessName)

	return process

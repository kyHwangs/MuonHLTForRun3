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


import FWCore.ParameterSet.Config as cms 

def replace_input_tag_module_label(tag,names_to_replace,suffix):
    if type(tag)==str: #having some problems with things appearing as strings....
        if tag in names_to_replace:
            tag = tag+suffix
    else:
        if tag.getModuleLabel() in names_to_replace:
            tag.setModuleLabel(tag.getModuleLabel()+suffix)
      
#replaces all input tags in the module which match modules to replace with that module name + suffix
def replace_input_tags(process,modname,pset,modules_to_replace,suffix):
    for paraname in pset.parameterNames_():
        para = pset.getParameter(paraname)
        if para.pythonTypeName()=="cms.PSet":
            replace_input_tags(process,modname,para,modules_to_replace,suffix)
        elif para.pythonTypeName()=="cms.VPSet":
            for newpset in para:
                replace_input_tags(process,modname,newpset,modules_to_replace,suffix)
        elif para.pythonTypeName()=="cms.InputTag":
            replace_input_tag_module_label(para,modules_to_replace,suffix)            
        elif para.pythonTypeName()=="cms.VInputTag":
            for tag in para: 
                replace_input_tag_module_label(tag,modules_to_replace,suffix)
        
                                                  
#clones all these egamma pat modules and then updates the tags of these modules
#to point to the other cloned modules
def miniAOD_addOrginalEGamma(process,suffix):
    modules_to_clone=["slimmedElectrons",
                      "selectedPatElectrons",
                      "patElectrons",
                      "slimmedPhotons",
                      "selectedPatPhotons",
                      "patPhotons",
                      "reducedEgamma",
                      "egmGsfElectronIDs",
                      "electronMVAValueMapProducer",
                      "electronRegressionValueMapProducer",
                      "egmPhotonIDs",
                      "photonIDValueMapProducer",
                      "photonRegressionValueMapProducer",
                      "photonMVAValueMapProducer",
                      #"particleBasedIsolation",
                      #"PhotonIDProdGED",
                      #"eidLoose",
                      #"eidRobustHighEnergy",
                      #"eidRobustLoose",
                      #"eidRobustTight",
                      #"eidTight",
                      #"photonEcalPFClusterIsolationProducer",
                      #"photonHcalPFClusterIsolationProducer",
                      #"phoEcalPFClusIso",
                      #"phoHcalPFClusIso",
                      #"electronEcalPFClusterIsolationProducer",
                      #"electronHcalPFClusterIsolationProducer",
                      #"eleEcalPFClusIso",
                      #"eleHcalPFClusIso",
                      "phPFIsoDepositChargedPAT",
                      "phPFIsoDepositChargedAllPAT",
                      "phPFIsoDepositPUPAT",
                      "phPFIsoDepositNeutralPAT",
                      "phPFIsoDepositGammaPAT",
                      "phPFIsoValueCharged04PFIdPAT",
                      "phPFIsoValueChargedAll04PFIdPAT",
                      "phPFIsoValuePU04PFIdPAT",
                      "phPFIsoValueNeutral04PFIdPAT",
                      "phPFIsoValueGamma04PFIdPAT",
                      "elPFIsoDepositChargedPAT",
                      "elPFIsoDepositChargedAllPAT",
                      "elPFIsoDepositPUPAT",
                      "elPFIsoDepositNeutralPAT",
                      "elPFIsoDepositGammaPAT",
                      "elPFIsoValueCharged04PFIdPAT",
                      "elPFIsoValueChargedAll04PFIdPAT",
                      "elPFIsoValuePU04PFIdPAT",
                      "elPFIsoValueNeutral04PFIdPAT",
                      "elPFIsoValueGamma04PFIdPAT",
                      "elPFIsoValueCharged04NoPFIdPAT",
                      "elPFIsoValueChargedAll04NoPFIdPAT",
                      "elPFIsoValuePU04NoPFIdPAT",
                      "elPFIsoValueNeutral04NoPFIdPAT",
                      "elPFIsoValueGamma04NoPFIdPAT"]
     

    for name in modules_to_clone:
        new_name = name+suffix
        setattr(process,new_name,getattr(process,name).clone())  
        replace_input_tags(process,new_name,getattr(process,new_name),modules_to_clone,suffix)
          




def customizeGSFixForPAT(process): 
    #this clones all the modules before they were modified to run on the orginal collections
    miniAOD_addOrginalEGamma(process,"BeforeGSFix")
    process.MINIAODoutput.outputCommands.extend(['keep *_reducedEgammaBeforeGSFix_*_*',
                                                 'keep *_slimmedElectronsBeforeGSFix_*_*',
                                                 'keep *_slimmedPhotonsBeforeGSFix_*_*'])
    process.reducedEgamma.gsfElectrons = cms.InputTag("gedGsfElectronsGSFixed")
    process.reducedEgamma.gsfElectronsPFValMap = cms.InputTag("particleBasedIsolationGSFixed","gedGsfElectrons")
    process.reducedEgamma.gsfElectronPFClusterIsoSources = cms.VInputTag(
        cms.InputTag("electronEcalPFClusterIsolationProducerGSFixed"),
        cms.InputTag("electronHcalPFClusterIsolationProducerGSFixed"),
        )
    process.reducedEgamma.gsfElectronIDSources = cms.VInputTag(
        cms.InputTag("eidLooseGSFixed"),
        cms.InputTag("eidRobustHighEnergyGSFixed"),
        cms.InputTag("eidRobustLooseGSFixed"),
        cms.InputTag("eidRobustTightGSFixed"),
        cms.InputTag("eidTightGSFixed"),
        )
    process.reducedEgamma.photons = cms.InputTag("gedPhotonsGSFixed")
    process.reducedEgamma.conversions = cms.InputTag("allConversionsGSFixed")
    process.reducedEgamma.singleConversions = cms.InputTag("particleFlowEGammaGSFixed")
    process.reducedEgamma.photonsPFValMap = cms.InputTag("particleBasedIsolationGSFixed","gedPhotons")
    process.reducedEgamma.photonPFClusterIsoSources = cms.VInputTag(
        cms.InputTag("photonEcalPFClusterIsolationProducerGSFixed"),
        cms.InputTag("photonHcalPFClusterIsolationProducerGSFixed"),
        )
    process.reducedEgamma.photonIDSources = cms.VInputTag(
        cms.InputTag("PhotonCutBasedIDLooseGSFixed"),
        cms.InputTag("PhotonCutBasedIDLooseEMGSFixed"),    
        cms.InputTag("PhotonCutBasedIDTightGSFixed")
        )
    process.reducedEgamma.barrelEcalHits = cms.InputTag("ecalMultiAndGSWeightRecHitEB")
    process.reducedEgamma.endcapEcalHits = cms.InputTag("reducedEcalRecHitsEE")
    process.reducedEgamma.preshowerEcalHits = cms.InputTag("reducedEcalRecHitsES")

    return process

#ifndef SiStripMonitorClient_SiStripDcsInfo_h
#define SiStripMonitorClient_SiStripDcsInfo_h
// -*- C++ -*-
//
// Package:     SiStripMonitorClient
// Class  :     SiStripDcsInfo
// 
/**\class SiStripDcsInfo SiStripDcsInfo.h DQM/SiStripMonitorCluster/interface/SiStripDcsInfo.h

 Description: 
      Checks the # of SiStrip FEDs from DAQ
 Usage:
    <usage>

*/
//
//          Author:  Suchandra Dutta
//         Created:  Mon Feb 16 19:00:00 CET 2009
//

#include <string>

#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/LuminosityBlock.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/Framework/interface/EventSetup.h"

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>

class DQMStore;
class MonitorElement;
class SiStripDetVOff;
class SiStripDetCabling; 

class SiStripDcsInfo: public edm::EDAnalyzer {

 public:

  /// Constructor
  SiStripDcsInfo(const edm::ParameterSet& ps);
  
  /// Destructor
  virtual ~SiStripDcsInfo();

 private:

  /// BeginJob
  void beginJob();

  /// Begin Run
  void beginRun(edm::Run const& run, edm::EventSetup const& eSetup);

  /// Begin Luminosity Block
  void beginLuminosityBlock(edm::LuminosityBlock const& lumiSeg, edm::EventSetup const& eSetup) ;

  /// End Of Luminosity
  void endLuminosityBlock(edm::LuminosityBlock const& lumiSeg, edm::EventSetup const& iSetup);

  /// EndRun
  void endRun(edm::Run const& run, edm::EventSetup const& eSetup);

  /// Analyze
  void analyze(edm::Event const&, edm::EventSetup const&);



private:
  void bookStatus();
  void readStatus(edm::EventSetup const&);
  void readCabling(edm::EventSetup const&);
  void addBadModules();
  void fillStatus();
  void fillDummyStatus();

  DQMStore* dqmStore_;
  MonitorElement * DcsFraction_;

  struct SubDetMEs{
    std::string folder_name;
    MonitorElement* DcsFractionME;
    int TotalDetectors;
    std::vector<uint32_t> FaultyDetectors;
  };

  std::map <std::string, SubDetMEs> SubDetMEsMap;
  unsigned long long m_cacheIDCabling_;
  unsigned long long m_cacheIDDcs_;
  bool bookedStatus_;

  edm::ESHandle<SiStripDetVOff> siStripDetVOff_;
  int  nFEDConnected_;

  int nLumiAnalysed_;

  edm::ESHandle< SiStripDetCabling > detCabling_;
};
#endif

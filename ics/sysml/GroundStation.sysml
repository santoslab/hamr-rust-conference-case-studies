//@ HAMR: --platform Microkit

package GroundStation {

    private import HAMR::*;

    part def Periodic_Rust_Thread :> Thread {
        attribute :>> Dispatch_Protocol = Periodic;
        attribute :>> Period = 1000 [ms];
        attribute :>> Stack_Size = 1048576 [byte];
        attribute :>> Implementation_Language = Rust;
    }

    part def WifiDriverVM_t :> Periodic_Rust_Thread {
        port wifiRecvIn: EventDataPort { in :>> type : Common::IncomingWifiMessage_Impl; }
        port wifiRecvOut: EventDataPort { out :>> type : Common::IncomingWifiMessage_Impl; }
        port wifiSendIn: EventDataPort { in :>> type : Common::OutgoingWifiMessage_Impl; }
        port wifiSendOut: EventDataPort { out :>> type : Common::OutgoingWifiMessage_Impl; }

        attribute :>> Compute_Execution_Time = 150 [ms] .. 150 [ms];
        attribute :>> Implementation_Language = C;
    }

    part def WifiDriver_t :> Periodic_Rust_Thread {
        port wifiRecv: EventDataPort { in :>> type : Common::IncomingWifiMessage_Impl; }
        port wifiSend: EventDataPort { out :>> type : Common::OutgoingWifiMessage_Impl; }
        port HMD_log: EventDataPort { out :>> type : Common::EncryptedMessage_Impl; }
        port analysis_report: EventDataPort { in :>> type : Common::OutgoingWifiMessage_Impl; }
        port analysis_request: EventDataPort { out :>> type : Common::AnalysisRequest_Impl; }
        in port alert_in: EventPort;

        language "GUMBO" /*{
            state
                alert_cmd: Base_Types::Boolean;

            initialize
                modifies alert_cmd;

                guarantee defaultAlert:
                    alert_cmd == false;

            compute
                modifies alert_cmd;

                assume IncomingAlert "A: A report should not be received if an alert is received.":
                    HasEvent(alert_in) implies not HasEvent(analysis_report);

                assume Trusted_Report "A: Reports received are to a trusted destination.":
                    HasEvent(analysis_report) implies
                        MATRICS_Model_Transformations::GUMBO__Library::FOUND_IN_ALLOW_LIST(
                            analysis_report.header.client);

                guarantee alert_cmd_variable "G: Once an alert command is seen, always stay alerted.":
                    alert_cmd == (HasEvent(alert_in) or In(alert_cmd));

                guarantee Process_Report "G: Stop outgoing communication once an alert has been received.":
                    if (HasEvent(analysis_report) & not alert_cmd) ?
                        (MustSend(wifiSend) & (wifiSend == analysis_report)) else
                        NoSend(wifiSend);
        }*/
    }

    part def DataManager_t :> Periodic_Rust_Thread {
        port HMD_log: EventDataPort { in :>> type : Common::Log_Impl; }
        port encrypted_log: EventDataPort { out :>> type : Common::StoredLogFile_Impl; }
        port request_log: EventDataPort { in :>> type : Common::AnalysisRequest_Impl; }
        port storage_request: EventDataPort { out :>> type : Common::AnalysisRequest_Impl; }
        port encrypted_response: EventDataPort { in :>> type : Common::EncryptedAnalysisResponse_Impl; }
        port response_log: EventDataPort { out :>> type : Common::AnalysisResponse_Impl; }
        in port zeroize: EventPort;

        language "GUMBO" /*{
            state
                zeroize_cmd: Base_Types::Boolean;

            functions
                def IS_ZEROIZED(
                    response: Common::Response_Impl): Base_Types::Boolean :=
                    MATRICS_Model_Transformations::GUMBO__Library::IS_NULL_REQUEST(
                        response.request) &
                    response.validLogCount == 0 [u32] &
                    response.moreAvailable == false &
                    response.nextStartTime == 0 [u64] &
                    ((0 .. size(response.logs) - 1) -> forAll { in response_log_index;
                        MATRICS_Model_Transformations::GUMBO__Library::IS_NULL_LOG(
                            response.logs#(response_log_index))
                    });

            initialize
                modifies zeroize_cmd;

                guarantee defaultZeroize:
                    zeroize_cmd == false;

            compute
                modifies zeroize_cmd;

                guarantee zeroize_cmd_variable "G: Once a zeroize command is seen, always zeroize.":
                    zeroize_cmd == (HasEvent(zeroize) or In(zeroize_cmd));

                guarantee Zeroize_Payload "G: Zeroize outgoing responses once an alert is received and when a request has been made.":
                    (zeroize_cmd & HasEvent(request_log)) implies
                        IS_ZEROIZED(response_log.payload);
        }*/
    }

    part def DataStorage_t :> Periodic_Rust_Thread {
        port encrypted_log: EventDataPort { in :>> type : Common::StoredLogFile_Impl; }
        port storage_request: EventDataPort { in :>> type : Common::AnalysisRequest_Impl; }
        port encrypted_response: EventDataPort { out :>> type : Common::EncryptedAnalysisResponse_Impl; }
        in port zeroize: EventPort;

        attribute :>> Implementation_Language = C;

        language "GUMBO" /*{
            state
                cache: Common::EncryptedLogArray_Impl;
                zeroize_cmd: Base_Types::Boolean;

            functions
                def IS_ZEROIZED_ENCRYPTED_MESSAGE(
                    encrypted_message: Common::EncryptedMessage_Impl): Base_Types::Boolean :=
                    ((0 .. size(encrypted_message.nonce) - 1) -> forAll { in nonce_index;
                        encrypted_message.nonce#(nonce_index) == 0 [u8]
                    }) &
                    ((0 .. size(encrypted_message.ciphertext) - 1) -> forAll { in ciphertext_index;
                        encrypted_message.ciphertext#(ciphertext_index) == 0 [u8]
                    }) &
                    ((0 .. size(encrypted_message.tag) - 1) -> forAll { in tag_index;
                        encrypted_message.tag#(tag_index) == 0 [u8]
                    });

                def IS_ZEROIZED_STORED_LOG_FILE(
                    file: Common::StoredLogFile_Impl): Base_Types::Boolean :=
                    IS_ZEROIZED_ENCRYPTED_MESSAGE(file.encryptedLog);

                def IS_ZEROIZED(
                    logs: Common::EncryptedLogArray_Impl): Base_Types::Boolean :=
                    ((0 .. size(logs) - 1) -> forAll { in stored_log_index;
                        IS_ZEROIZED_STORED_LOG_FILE(logs#(stored_log_index))
                    });

            initialize
                modifies zeroize_cmd;

                guarantee defaultZeroize:
                    zeroize_cmd == false;

            compute
                modifies cache, zeroize_cmd;

                guarantee zeroize_cmd_variable "G: Once a zeroize command is seen, always zeroize.":
                    zeroize_cmd == (HasEvent(zeroize) or In(zeroize_cmd));

                guarantee Zeroize_Cache "G: Zeroize cache once an alert is received.":
                    zeroize_cmd implies IS_ZEROIZED(cache);
        }*/
    }

    part def DataAnalysis_t :> Periodic_Rust_Thread {
        port request_log: EventDataPort { out :>> type : Common::AnalysisRequest_Impl; }
        port response_log: EventDataPort { in :>> type : Common::AnalysisResponse_Impl; }
        port analysis_report: EventDataPort { out :>> type : Common::AnalysisResponse_Impl; }
        port analysis_request: EventDataPort { in :>> type : Common::AnalysisRequest_Impl; }

        language "GUMBO" /*{
            compute
                assume Trusted_Request "A: Requests received are from a trusted source.":
                    HasEvent(analysis_request) implies
                        MATRICS_Model_Transformations::GUMBO__Library::FOUND_IN_ALLOW_LIST(
                            analysis_request.header.client);
        }*/
    }

    part def BtDriver_t :> Periodic_Rust_Thread {
        port btRecv: EventDataPort { in :>> type : Common::DummyMessage_Impl; }
        port btSend: EventDataPort { out :>> type : Common::DummyMessage_Impl; }
    }

    part def UsbDriver_t :> Periodic_Rust_Thread {
        port usbRecv: EventDataPort { in :>> type : Common::DummyMessage_Impl; }
        port usbSend: EventDataPort { out :>> type : Common::DummyMessage_Impl; }
    }

    part def LogMonitor_t :> Periodic_Rust_Thread {
        port request_log: EventDataPort { in :>> type : Common::AnalysisRequest_Impl; }
        port response_log_in: EventDataPort { in :>> type : Common::AnalysisResponse_Impl; }
        port response_log_out: EventDataPort { out :>> type : Common::AnalysisResponse_Impl; }
        out port alert_out: EventPort;
        out port storage_alert_out: EventPort;

        language "GUMBO" /*{
            state
                since_result: Base_Types::Boolean;
                is_valid: Base_Types::Boolean;
                historically_no_alert_cmd: Base_Types::Boolean;

            initialize
                modifies since_result, historically_no_alert_cmd;

                guarantee defaultSince:
                    since_result == false;

                guarantee defaultHistorically:
                    historically_no_alert_cmd == true;

            compute
                modifies since_result, is_valid, historically_no_alert_cmd;

                guarantee is_valid_variable "G: is_valid set correctly":
                    is_valid ==
                        (if (HasEvent(request_log) & HasEvent(response_log_in)) ?
                            true else
                            (HasEvent(response_log_in) implies In(since_result)));

                guarantee since_result_variable "G: since_result is equivalent to (not response_log_in event) Since (request_log event)":
                    since_result == GUMBO_PLTL::GUMBO__Library::AGREE_Since(
                        not HasEvent(response_log_in),
                        HasEvent(request_log),
                        In(since_result));

                guarantee historically_no_alert_cmd_variable "G: historically_no_alert_cmd is true if and only if no alert has been sent.":
                    historically_no_alert_cmd ==
                        (In(historically_no_alert_cmd) & not HasEvent(alert_out));

                guarantee Send_Alert "G: Send an alert if more than one response is received without a request.":
                    if (HasEvent(response_log_in) & not is_valid) ?
                        (MustSend(alert_out) & MustSend(storage_alert_out)) else
                        (NoSend(alert_out) & NoSend(storage_alert_out));

                guarantee Forward_Response "G: Only forward a response if a valid request has been made.":
                    if (HasEvent(response_log_in) & historically_no_alert_cmd) ?
                        (MustSend(response_log_out) & (response_log_out == response_log_in)) else
                        NoSend(response_log_out);
        }*/
    }

    part def ReportMonitor_t :> Periodic_Rust_Thread {
        port analysis_request: EventDataPort { in :>> type : Common::AnalysisRequest_Impl; }
        port analysis_report_in: EventDataPort { in :>> type : Common::OutgoingWifiMessage_Impl; }
        port analysis_report_out: EventDataPort { out :>> type : Common::OutgoingWifiMessage_Impl; }
        out port alert_out: EventPort;

        language "GUMBO" /*{
            state
                counter: Base_Types::Unsigned_32;
                since_result: Base_Types::Boolean;
                is_valid1: Base_Types::Boolean;
                is_invalid2: Base_Types::Boolean;

            functions
                def Counter(
                    i: Base_Types::Boolean,
                    reset: Base_Types::Boolean,
                    count: Base_Types::Unsigned_32): Base_Types::Unsigned_32 :=
                    if (reset) ?
                        0 [u32] else
                        (if (i) ? count + 1 [u32] else count);

            initialize
                modifies counter, since_result;

                guarantee defaultCounterAndSince:
                    counter == 0 [u32] & since_result == false;

            compute
                modifies counter, since_result, is_valid1, is_invalid2;

                guarantee counter_variable "G: counter set correctly":
                    counter == Counter(
                        HasEvent(analysis_request),
                        HasEvent(analysis_report_in),
                        In(counter));

                guarantee since_result_variable "G: Internal variable since_result is equivalent to (not analysis_report_in event) Since (analysis_request event)":
                    since_result == GUMBO_PLTL::GUMBO__Library::AGREE_Since(
                        not HasEvent(analysis_report_in),
                        HasEvent(analysis_request),
                        In(since_result));

                guarantee valid1 "G: is_valid1 set correctly":
                    if (HasEvent(analysis_report_in) & HasEvent(analysis_request)) ?
                        (is_valid1 == true) else
                        (is_valid1 == (HasEvent(analysis_report_in) implies In(since_result)));

                guarantee invalid2 "G: is_invalid2 set correctly":
                    is_invalid2 == (counter >= 3 [u32]);

                guarantee Send_Alert "G: Send an alert if a report is received without a valid request or if three or more requests are received without a report.":
                    if ((HasEvent(analysis_report_in) & not is_valid1) or is_invalid2) ?
                        MustSend(alert_out) else
                        NoSend(alert_out);

                guarantee Forward_Report "G: Only forward a report if a valid request has been made and it is to a trusted destination.":
                    if (HasEvent(analysis_report_in) & is_valid1 & not is_invalid2 &
                        MATRICS_Model_Transformations::GUMBO__Library::FOUND_IN_ALLOW_LIST(
                            analysis_report_in.header.client)) ?
                        (MustSend(analysis_report_out) &
                            (analysis_report_out == analysis_report_in)) else
                        NoSend(analysis_report_out);
        }*/
    }

    part def Decryptor_t :> Periodic_Rust_Thread {
        port HMD_log_in: EventDataPort { in :>> type : Common::EncryptedMessage_Impl; }
        port HMD_log_out: EventDataPort { out :>> type : Common::Log_Impl; }

        language "GUMBO" /*{
            compute
                guarantee Payload_Decrypted "G: Outgoing payload is decrypted.":
                    HasEvent(HMD_log_in) implies
                        MATRICS_Model_Transformations::GUMBO__Library::AES_128_GCM_DECRYPTS_LOG(
                            HMD_log_in,
                            HMD_log_out);
        }*/
    }

    part def Encryptor_t :> Periodic_Rust_Thread {
        port analysis_report_in: EventDataPort { in :>> type : Common::AnalysisResponse_Impl; }
        port analysis_report_out: EventDataPort { out :>> type : Common::OutgoingWifiMessage_Impl; }

        language "GUMBO" /*{
            compute
                guarantee Payload_Encrypted "G: Outgoing payload is encrypted.":
                    HasEvent(analysis_report_in) implies
                        MATRICS_Model_Transformations::GUMBO__Library::AES_128_GCM_ENCRYPTS_RESPONSE(
                            analysis_report_in.payload,
                            analysis_report_out.payload);

                guarantee Header_Unencrypted "G: Outgoing header is not encrypted.":
                    analysis_report_out.header == analysis_report_in.header;
        }*/
    }

    part def Firewall_t :> Periodic_Rust_Thread {
        port analysis_request_in: EventDataPort { in :>> type : Common::AnalysisRequest_Impl; }
        port analysis_request_out: EventDataPort { out :>> type : Common::AnalysisRequest_Impl; }

        language "GUMBO" /*{
            compute
                guarantee Forward_Request "G: Only forward a request if it is from a trusted source.":
                    if (HasEvent(analysis_request_in) &
                        MATRICS_Model_Transformations::GUMBO__Library::FOUND_IN_ALLOW_LIST(
                            analysis_request_in.header.client)) ?
                        (MustSend(analysis_request_out) &
                            (analysis_request_out == analysis_request_in)) else
                        NoSend(analysis_request_out);
        }*/
    }

    part def WifiDriverVM_p :> Process {
        port wifiRecvIn: EventDataPort { in :>> type : Common::IncomingWifiMessage_Impl; }
        port wifiRecvOut: EventDataPort { out :>> type : Common::IncomingWifiMessage_Impl; }
        port wifiSendIn: EventDataPort { in :>> type : Common::OutgoingWifiMessage_Impl; }
        port wifiSendOut: EventDataPort { out :>> type : Common::OutgoingWifiMessage_Impl; }

        part wifiDriver: WifiDriverVM_t;

        connection c1: PortConnection connect wifiRecvIn to wifiDriver.wifiRecvIn;
        connection c2: PortConnection connect wifiDriver.wifiRecvOut to wifiRecvOut;
        connection c3: PortConnection connect wifiSendIn to wifiDriver.wifiSendIn;
        connection c4: PortConnection connect wifiDriver.wifiSendOut to wifiSendOut;

        attribute :>> Domain = 2;
    }

    part def WifiDriver_p :> Process {
        port wifiRecv: EventDataPort { in :>> type : Common::IncomingWifiMessage_Impl; }
        port wifiSend: EventDataPort { out :>> type : Common::OutgoingWifiMessage_Impl; }
        port HMD_log: EventDataPort { out :>> type : Common::EncryptedMessage_Impl; }
        port analysis_report: EventDataPort { in :>> type : Common::OutgoingWifiMessage_Impl; }
        port analysis_request: EventDataPort { out :>> type : Common::AnalysisRequest_Impl; }
        in port alert_in: EventPort;

        part wifiDriver: WifiDriver_t;

        connection c1: PortConnection connect wifiRecv to wifiDriver.wifiRecv;
        connection c2: PortConnection connect analysis_report to wifiDriver.analysis_report;
        connection c3: PortConnection connect wifiDriver.wifiSend to wifiSend;
        connection c4: PortConnection connect wifiDriver.HMD_log to HMD_log;
        connection c5: PortConnection connect wifiDriver.analysis_request to analysis_request;
        connection c6: PortConnection connect alert_in to wifiDriver.alert_in;

        attribute :>> Domain = 3;
    }

    part def Decryptor_p :> Process {
        port HMD_log_in: EventDataPort { in :>> type : Common::EncryptedMessage_Impl; }
        port HMD_log_out: EventDataPort { out :>> type : Common::Log_Impl; }

        part decryptor: Decryptor_t;

        connection c1: PortConnection connect HMD_log_in to decryptor.HMD_log_in;
        connection c2: PortConnection connect decryptor.HMD_log_out to HMD_log_out;

        attribute :>> Domain = 4;
    }

    part def Firewall_p :> Process {
        port analysis_request_in: EventDataPort { in :>> type : Common::AnalysisRequest_Impl; }
        port analysis_request_out: EventDataPort { out :>> type : Common::AnalysisRequest_Impl; }

        part firewall: Firewall_t;

        connection c1: PortConnection connect analysis_request_in to firewall.analysis_request_in;
        connection c2: PortConnection connect firewall.analysis_request_out to analysis_request_out;

        attribute :>> Domain = 5;
    }

    part def DataAnalysis_p :> Process {
        port request_log: EventDataPort { out :>> type : Common::AnalysisRequest_Impl; }
        port response_log: EventDataPort { in :>> type : Common::AnalysisResponse_Impl; }
        port analysis_report: EventDataPort { out :>> type : Common::AnalysisResponse_Impl; }
        port analysis_request: EventDataPort { in :>> type : Common::AnalysisRequest_Impl; }

        part dataAnalysis: DataAnalysis_t;

        connection c1: PortConnection connect response_log to dataAnalysis.response_log;
        connection c2: PortConnection connect analysis_request to dataAnalysis.analysis_request;
        connection c3: PortConnection connect dataAnalysis.request_log to request_log;
        connection c4: PortConnection connect dataAnalysis.analysis_report to analysis_report;

        attribute :>> Domain = 6;
    }

    part def DataManager_p :> Process {
        port HMD_log: EventDataPort { in :>> type : Common::Log_Impl; }
        port encrypted_log: EventDataPort { out :>> type : Common::StoredLogFile_Impl; }
        port request_log: EventDataPort { in :>> type : Common::AnalysisRequest_Impl; }
        port storage_request: EventDataPort { out :>> type : Common::AnalysisRequest_Impl; }
        port encrypted_response: EventDataPort { in :>> type : Common::EncryptedAnalysisResponse_Impl; }
        port response_log: EventDataPort { out :>> type : Common::AnalysisResponse_Impl; }
        in port zeroize: EventPort;

        part dataManager: DataManager_t;

        connection c1: PortConnection connect HMD_log to dataManager.HMD_log;
        connection c2: PortConnection connect request_log to dataManager.request_log;
        connection c3: PortConnection connect dataManager.response_log to response_log;
        connection c4: PortConnection connect dataManager.encrypted_log to encrypted_log;
        connection c5: PortConnection connect dataManager.storage_request to storage_request;
        connection c6: PortConnection connect encrypted_response to dataManager.encrypted_response;
        connection c7: PortConnection connect zeroize to dataManager.zeroize;

        attribute :>> Domain = 7;
    }

    part def LogMonitor_p :> Process {
        port request_log: EventDataPort { in :>> type : Common::AnalysisRequest_Impl; }
        port response_log_in: EventDataPort { in :>> type : Common::AnalysisResponse_Impl; }
        port response_log_out: EventDataPort { out :>> type : Common::AnalysisResponse_Impl; }
        out port alert_out: EventPort;
        out port storage_alert_out: EventPort;

        part logMonitor: LogMonitor_t;

        connection c1: PortConnection connect request_log to logMonitor.request_log;
        connection c2: PortConnection connect response_log_in to logMonitor.response_log_in;
        connection c3: PortConnection connect logMonitor.response_log_out to response_log_out;
        connection c4: PortConnection connect logMonitor.alert_out to alert_out;
        connection c5: PortConnection connect logMonitor.storage_alert_out to storage_alert_out;

        attribute :>> Domain = 8;
    }

    part def Encryptor_p :> Process {
        port analysis_report_in: EventDataPort { in :>> type : Common::AnalysisResponse_Impl; }
        port analysis_report_out: EventDataPort { out :>> type : Common::OutgoingWifiMessage_Impl; }

        part encryptor: Encryptor_t;

        connection c1: PortConnection connect analysis_report_in to encryptor.analysis_report_in;
        connection c2: PortConnection connect encryptor.analysis_report_out to analysis_report_out;

        attribute :>> Domain = 9;
    }

    part def ReportMonitor_p :> Process {
        port analysis_request: EventDataPort { in :>> type : Common::AnalysisRequest_Impl; }
        port analysis_report_in: EventDataPort { in :>> type : Common::OutgoingWifiMessage_Impl; }
        port analysis_report_out: EventDataPort { out :>> type : Common::OutgoingWifiMessage_Impl; }
        out port alert_out: EventPort;

        part reportMonitor: ReportMonitor_t;

        connection c1: PortConnection connect analysis_request to reportMonitor.analysis_request;
        connection c2: PortConnection connect analysis_report_in to reportMonitor.analysis_report_in;
        connection c3: PortConnection connect reportMonitor.analysis_report_out to analysis_report_out;
        connection c4: PortConnection connect reportMonitor.alert_out to alert_out;

        attribute :>> Domain = 10;
    }

    part def BtDriver_p :> Process {
        port btRecv: EventDataPort { in :>> type : Common::DummyMessage_Impl; }
        port btSend: EventDataPort { out :>> type : Common::DummyMessage_Impl; }

        part btDriver: BtDriver_t;

        connection c1: PortConnection connect btRecv to btDriver.btRecv;
        connection c2: PortConnection connect btDriver.btSend to btSend;

        attribute :>> Domain = 11;
    }

    part def UsbDriver_p :> Process {
        port usbRecv: EventDataPort { in :>> type : Common::DummyMessage_Impl; }
        port usbSend: EventDataPort { out :>> type : Common::DummyMessage_Impl; }

        part usbDriver: UsbDriver_t;

        connection c1: PortConnection connect usbRecv to usbDriver.usbRecv;
        connection c2: PortConnection connect usbDriver.usbSend to usbSend;

        attribute :>> Domain = 12;
    }

    part def DataStorage_p :> Process {
        port encrypted_log: EventDataPort { in :>> type : Common::StoredLogFile_Impl; }
        port storage_request: EventDataPort { in :>> type : Common::AnalysisRequest_Impl; }
        port encrypted_response: EventDataPort { out :>> type : Common::EncryptedAnalysisResponse_Impl; }
        in port zeroize: EventPort;

        part dataStorage: DataStorage_t;

        connection c1: PortConnection connect encrypted_log to dataStorage.encrypted_log;
        connection c2: PortConnection connect storage_request to dataStorage.storage_request;
        connection c3: PortConnection connect dataStorage.encrypted_response to encrypted_response;
        connection c4: PortConnection connect zeroize to dataStorage.zeroize;

        attribute :>> Domain = 13;
    }

    part def WifiDriver_sys :> System {
        port wifiRecv: EventDataPort { in :>> type : Common::IncomingWifiMessage_Impl; }
        port wifiSend: EventDataPort { out :>> type : Common::OutgoingWifiMessage_Impl; }
        port HMD_log: EventDataPort { out :>> type : Common::EncryptedMessage_Impl; }
        port analysis_report: EventDataPort { in :>> type : Common::OutgoingWifiMessage_Impl; }
        port analysis_request: EventDataPort { out :>> type : Common::AnalysisRequest_Impl; }
        in port alert_in: EventPort;

        part wifiDriver: WifiDriver_p;
        part wifiDriverVM: WifiDriverVM_p;

        connection c1: PortConnection connect wifiRecv to wifiDriverVM.wifiRecvIn;
        connection c2: PortConnection connect wifiDriverVM.wifiRecvOut to wifiDriver.wifiRecv;
        connection c3: PortConnection connect wifiDriver.wifiSend to wifiDriverVM.wifiSendIn;
        connection c4: PortConnection connect wifiDriverVM.wifiSendOut to wifiSend;
        connection c5: PortConnection connect wifiDriver.HMD_log to HMD_log;
        connection c6: PortConnection connect analysis_report to wifiDriver.analysis_report;
        connection c7: PortConnection connect wifiDriver.analysis_request to analysis_request;
        connection c8: PortConnection connect alert_in to wifiDriver.alert_in;
    }

    part def DataManager_sys :> System {
        port HMD_log: EventDataPort { in :>> type : Common::Log_Impl; }
        port request_log: EventDataPort { in :>> type : Common::AnalysisRequest_Impl; }
        port response_log: EventDataPort { out :>> type : Common::AnalysisResponse_Impl; }
        in port zeroize: EventPort;
        in port storage_zeroize: EventPort;

        part dataManager: DataManager_p;
        part dataStorage: DataStorage_p;

        connection c1: PortConnection connect HMD_log to dataManager.HMD_log;
        connection c2: PortConnection connect request_log to dataManager.request_log;
        connection c3: PortConnection connect dataManager.response_log to response_log;
        connection c4: PortConnection connect dataManager.encrypted_log to dataStorage.encrypted_log;
        connection c5: PortConnection connect storage_zeroize to dataStorage.zeroize;
        connection c6: PortConnection connect zeroize to dataManager.zeroize;
        connection c7: PortConnection connect dataManager.storage_request to dataStorage.storage_request;
        connection c8: PortConnection connect dataStorage.encrypted_response to dataManager.encrypted_response;
    }

    part def SW_seL4_hardened :> System {
        port wifiRecv: EventDataPort { in :>> type : Common::IncomingWifiMessage_Impl; }
        port wifiSend: EventDataPort { out :>> type : Common::OutgoingWifiMessage_Impl; }
        port btRecv: EventDataPort { in :>> type : Common::DummyMessage_Impl; }
        port btSend: EventDataPort { out :>> type : Common::DummyMessage_Impl; }
        port usbRecv: EventDataPort { in :>> type : Common::DummyMessage_Impl; }
        port usbSend: EventDataPort { out :>> type : Common::DummyMessage_Impl; }

        part wifiDriver: WifiDriver_sys;
        part btDriver: BtDriver_p;
        part usbDriver: UsbDriver_p;
        part dataManager: DataManager_sys;
        part dataAnalysis: DataAnalysis_p;
        part decryptor: Decryptor_p;
        part encryptor: Encryptor_p;
        part logMonitor: LogMonitor_p;
        part reportMonitor: ReportMonitor_p;
        part firewall: Firewall_p;

        connection c1: PortConnection connect wifiRecv to wifiDriver.wifiRecv;
        connection c2: PortConnection connect wifiDriver.wifiSend to wifiSend;
        connection c5: PortConnection connect btRecv to btDriver.btRecv;
        connection c6: PortConnection connect btDriver.btSend to btSend;
        connection c7: PortConnection connect usbRecv to usbDriver.usbRecv;
        connection c8: PortConnection connect usbDriver.usbSend to usbSend;
        connection c9: PortConnection connect dataAnalysis.request_log to dataManager.request_log;
        connection c10: PortConnection connect wifiDriver.HMD_log to decryptor.HMD_log_in;
        connection c11: PortConnection connect decryptor.HMD_log_out to dataManager.HMD_log;
        connection c12: PortConnection connect dataAnalysis.analysis_report to encryptor.analysis_report_in;
        connection c13: PortConnection connect reportMonitor.analysis_report_out to wifiDriver.analysis_report;
        connection c14: PortConnection connect dataAnalysis.request_log to logMonitor.request_log;
        connection c15: PortConnection connect dataManager.response_log to logMonitor.response_log_in;
        connection c16: PortConnection connect logMonitor.response_log_out to dataAnalysis.response_log;
        connection c17: PortConnection connect logMonitor.alert_out to dataManager.zeroize;
        connection c17_storage: PortConnection connect logMonitor.storage_alert_out to dataManager.storage_zeroize;
        connection c18: PortConnection connect wifiDriver.analysis_request to reportMonitor.analysis_request;
        connection c19: PortConnection connect encryptor.analysis_report_out to reportMonitor.analysis_report_in;
        connection c20: PortConnection connect reportMonitor.alert_out to wifiDriver.alert_in;
        connection c21: PortConnection connect wifiDriver.analysis_request to firewall.analysis_request_in;
        connection c22: PortConnection connect firewall.analysis_request_out to dataAnalysis.analysis_request;
    }

    part def Proc :> Processor {
        attribute :>> Frame_Period = 1000 [ms];
        attribute :>> Clock_Period = 1 [ms];
        attribute :>> Max_Domain = 15;
    }

    part def virt_proc :> VirtualProcessor;

    part def GroundStation_Impl :> System {
        port wifiRecv: EventDataPort { in :>> type : Common::IncomingWifiMessage_Impl; }
        port wifiSend: EventDataPort { out :>> type : Common::OutgoingWifiMessage_Impl; }
        port btRecv: EventDataPort { in :>> type : Common::DummyMessage_Impl; }
        port btSend: EventDataPort { out :>> type : Common::DummyMessage_Impl; }
        port usbRecv: EventDataPort { in :>> type : Common::DummyMessage_Impl; }
        port usbSend: EventDataPort { out :>> type : Common::DummyMessage_Impl; }

        part cpu: Proc;
        part vcpu: virt_proc;
        part storage_vcpu: virt_proc;

        part cpuSw_wifiDriver_wifiDriver: WifiDriver_p;
        part cpuSw_wifiDriver_wifiDriverVM: WifiDriverVM_p;
        part cpuSw_btDriver: BtDriver_p;
        part cpuSw_usbDriver: UsbDriver_p;
        part cpuSw_dataManager_dataManager: DataManager_p;
        part cpuSw_dataManager_dataStorage: DataStorage_p;
        part cpuSw_dataAnalysis: DataAnalysis_p;
        part cpuSw_decryptor: Decryptor_p;
        part cpuSw_encryptor: Encryptor_p;
        part cpuSw_logMonitor: LogMonitor_p;
        part cpuSw_reportMonitor: ReportMonitor_p;
        part cpuSw_firewall: Firewall_p;

        connection c1: PortConnection connect wifiRecv to cpuSw_wifiDriver_wifiDriverVM.wifiRecvIn;
        connection c2: PortConnection connect cpuSw_wifiDriver_wifiDriverVM.wifiRecvOut to cpuSw_wifiDriver_wifiDriver.wifiRecv;
        connection c3: PortConnection connect cpuSw_wifiDriver_wifiDriver.wifiSend to cpuSw_wifiDriver_wifiDriverVM.wifiSendIn;
        connection c4: PortConnection connect cpuSw_wifiDriver_wifiDriverVM.wifiSendOut to wifiSend;
        connection c5: PortConnection connect btRecv to cpuSw_btDriver.btRecv;
        connection c6: PortConnection connect cpuSw_btDriver.btSend to btSend;
        connection c7: PortConnection connect usbRecv to cpuSw_usbDriver.usbRecv;
        connection c8: PortConnection connect cpuSw_usbDriver.usbSend to usbSend;
        connection c9: PortConnection connect cpuSw_dataAnalysis.request_log to cpuSw_dataManager_dataManager.request_log;
        connection c10: PortConnection connect cpuSw_wifiDriver_wifiDriver.HMD_log to cpuSw_decryptor.HMD_log_in;
        connection c11: PortConnection connect cpuSw_decryptor.HMD_log_out to cpuSw_dataManager_dataManager.HMD_log;
        connection c12: PortConnection connect cpuSw_dataAnalysis.analysis_report to cpuSw_encryptor.analysis_report_in;
        connection c13: PortConnection connect cpuSw_reportMonitor.analysis_report_out to cpuSw_wifiDriver_wifiDriver.analysis_report;
        connection c14: PortConnection connect cpuSw_dataAnalysis.request_log to cpuSw_logMonitor.request_log;
        connection c15: PortConnection connect cpuSw_dataManager_dataManager.response_log to cpuSw_logMonitor.response_log_in;
        connection c16: PortConnection connect cpuSw_logMonitor.response_log_out to cpuSw_dataAnalysis.response_log;
        connection c17_dataManager: PortConnection connect cpuSw_logMonitor.alert_out to cpuSw_dataManager_dataManager.zeroize;
        connection c17_dataStorage: PortConnection connect cpuSw_logMonitor.storage_alert_out to cpuSw_dataManager_dataStorage.zeroize;
        connection c18: PortConnection connect cpuSw_wifiDriver_wifiDriver.analysis_request to cpuSw_reportMonitor.analysis_request;
        connection c19: PortConnection connect cpuSw_encryptor.analysis_report_out to cpuSw_reportMonitor.analysis_report_in;
        connection c20: PortConnection connect cpuSw_reportMonitor.alert_out to cpuSw_wifiDriver_wifiDriver.alert_in;
        connection c21: PortConnection connect cpuSw_wifiDriver_wifiDriver.analysis_request to cpuSw_firewall.analysis_request_in;
        connection c22: PortConnection connect cpuSw_firewall.analysis_request_out to cpuSw_dataAnalysis.analysis_request;
        connection dataManager_c4: PortConnection connect cpuSw_dataManager_dataManager.encrypted_log to cpuSw_dataManager_dataStorage.encrypted_log;
        connection dataManager_c7: PortConnection connect cpuSw_dataManager_dataManager.storage_request to cpuSw_dataManager_dataStorage.storage_request;
        connection dataManager_c8: PortConnection connect cpuSw_dataManager_dataStorage.encrypted_response to cpuSw_dataManager_dataManager.encrypted_response;

        allocation vm_binding: Deployment_Properties::Actual_Processor_Binding
            allocate cpuSw_wifiDriver_wifiDriverVM to vcpu;
        allocation data_storage_vm_binding: Deployment_Properties::Actual_Processor_Binding
            allocate cpuSw_dataManager_dataStorage to storage_vcpu;
        allocation vcpu_binding: Deployment_Properties::Actual_Processor_Binding
            allocate vcpu to cpu;
        allocation storage_vcpu_binding: Deployment_Properties::Actual_Processor_Binding
            allocate storage_vcpu to cpu;
        allocation wifi_driver_binding: Deployment_Properties::Actual_Processor_Binding
            allocate cpuSw_wifiDriver_wifiDriver to cpu;
        allocation bt_driver_binding: Deployment_Properties::Actual_Processor_Binding
            allocate cpuSw_btDriver to cpu;
        allocation usb_driver_binding: Deployment_Properties::Actual_Processor_Binding
            allocate cpuSw_usbDriver to cpu;
        allocation data_manager_binding: Deployment_Properties::Actual_Processor_Binding
            allocate cpuSw_dataManager_dataManager to cpu;
        allocation data_analysis_binding: Deployment_Properties::Actual_Processor_Binding
            allocate cpuSw_dataAnalysis to cpu;
        allocation decryptor_binding: Deployment_Properties::Actual_Processor_Binding
            allocate cpuSw_decryptor to cpu;
        allocation encryptor_binding: Deployment_Properties::Actual_Processor_Binding
            allocate cpuSw_encryptor to cpu;
        allocation log_monitor_binding: Deployment_Properties::Actual_Processor_Binding
            allocate cpuSw_logMonitor to cpu;
        allocation report_monitor_binding: Deployment_Properties::Actual_Processor_Binding
            allocate cpuSw_reportMonitor to cpu;
        allocation firewall_binding: Deployment_Properties::Actual_Processor_Binding
            allocate cpuSw_firewall to cpu;

        attribute :>> Scheduling = MCS;

    }

}

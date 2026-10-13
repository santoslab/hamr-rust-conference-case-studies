//@ HAMR: --platform Microkit --scheduling UserLand --output-dir ../hamr --sel4-output-dir ../hamr/microkit_mcs

package SW {

    private import HAMR::*;
    private import GumboLib::*;

    // ==========================================================================
    //   D a t a    T y p e s
    // ==========================================================================

    enum def InternetProtocol {
        enum IPV4;
        enum IPV6;
    }

    enum def FrameProtocol {
        enum TCP;
        enum ARP;
    }

    enum def ARP_Type {
        enum REQUEST;
        enum REPLY;
        enum NA;
    }

    // CR-01: cyber-mode awareness types (see action-requests/CR-01-add-RTL-mode/)
    enum def Mode {
        enum Init;
        enum Normal;
        enum RTL;
    }

    enum def AttackStatus {
        enum OK;
        enum Attack;
    }

    part def RawEthernetMessage :> Array {
        part :>> Base_Type : Base_Types::Unsigned_8;

        attribute :>> Dimensions = 1600;

        attribute :>> Array_Size_Kind = Array_Size_Kinds::Fixed;

        attribute :>> Data_Size = 1600[byte];
    }

    part def StructuredEthernetMessage_i :> Data {
        part malformedFrame : Base_Types::Boolean;
        attribute internetProtocol : InternetProtocol;
        attribute frameProtocol : FrameProtocol;
        part portIsWhitelisted : Base_Types::Boolean;
        attribute arpType : ARP_Type;
        part rawMessage : RawEthernetMessage;

        language "GUMBO" /*{
            invariants
                inv relateFrameProtocolToArpType:
                    (frameProtocol == SW::FrameProtocol.TCP & arpType == SW::ARP_Type.NA) |
                    (frameProtocol == SW::FrameProtocol.ARP &
                        (arpType == SW::ARP_Type.REQUEST | arpType == SW::ARP_Type.REPLY));
        }*/
    }

    // ==========================================================================
    //   T h r e a d s
    // ==========================================================================

    // Default thread configuration

    part def Periodic_Rust_Thread :> Thread {
        attribute :>> Period = 1000[ms];
        attribute :>> Dispatch_Protocol = Supported_Dispatch_Protocols::Periodic;
        attribute :>> Implementation_Language = Implementation_Languages::Rust;
        attribute :>> Compute_Execution_Time = 100[ms] .. 100[ms] as Compute_Execution_Time;
        attribute :>> Stack_Size = 1048576[byte] as Size;
    }

    // ----------------------------------------------------------
    //   Thread   L o w - L e v e l    E t h e r n e t   D r i v e r 
    // ----------------------------------------------------------

    part def LowLevelEthernetDriver_i :> Periodic_Rust_Thread {
        // Ethernet Frames: Raw Ethernet frames received from the physical network interface.
        port EthernetFramesRx: EventDataPort { out :>> type : StructuredEthernetMessage_i; }
        port EthernetFramesTx: EventDataPort { in :>> type : StructuredEthernetMessage_i; }
    }

    // -----------------------------------------------------
    //   Thread   R x   F i r e w a l l
    // -----------------------------------------------------

    part def Firewall_Rx_i :> Periodic_Rust_Thread {
        port EthernetFramesRxIn:  EventDataPort { in :>> type : StructuredEthernetMessage_i; }
        port EthernetFramesRxOut: EventDataPort { out :>> type : StructuredEthernetMessage_i; }

        // CR-01: mode awareness + attack detection (DataPorts per RD-4)
        port CurrentMode:    DataPort { in  :>> type : Mode; }
        port AttackStatusRx: DataPort { out :>> type : AttackStatus; }

        language "GUMBO" /*{
            state
                malformedCount: Base_Types::Integer_32;

            initialize
                modifies (malformedCount);
                guarantee CR01_Rx_Init "FirewallRx_Req_Init: malformed count starts at zero; attack status DataPort initialized to OK.":
                    malformedCount == 0 [i32] &
                    AttackStatusRx == SW::AttackStatus.OK;

            compute
                modifies (malformedCount);

                guarantee RC_INSPECTA_00_HLR_1 "1.1 firewall: no frame in RxOut if no frame in RxIn (RC_INSPECTA_00-HLR-1) The firewall shall not have any frame in RxOut if there are no frame in RxIn.":
                    (not HasEvent(EthernetFramesRxIn))
                        implies NoSend(EthernetFramesRxOut);

                guarantee RC_INSPECTA_00_HLR_2 "1.2 firewall: drop malformed frames (RC_INSPECTA_00-HLR-1) The firewall shall drop any frame that is malformed.":
                    (HasEvent(EthernetFramesRxIn) implies
                        '->:' (GumboLib::GUMBO__Library::isMalformedFrame(EthernetFramesRxIn),
                            NoSend(EthernetFramesRxOut)));

                guarantee RC_INSPECTA_00_HLR_4 "1.4 firewall: drop ipv6 frames (RC_INSPECTA_00-HLR-2) The firewall shall drop any frame that is type ipv6.":
                    (HasEvent(EthernetFramesRxIn) implies
                        '->:' (GumboLib::GUMBO__Library::isIPV6(EthernetFramesRxIn),
                            NoSend(EthernetFramesRxOut)));

                guarantee RC_INSPECTA_00_HLR_6 "1.6 firewall: drop RxIn ipv4 arp frames (RC_INSPECTA_00-HLR-4) The firewall shall drop any frame from RxIn that is an Ipv4 frame whose protocol is ARP.":
                    (HasEvent(EthernetFramesRxIn) implies
                        '->:' (GumboLib::GUMBO__Library::isARP(EthernetFramesRxIn),
                            NoSend(EthernetFramesRxOut)));

                guarantee RC_INSPECTA_00_HLR_8 "1.8 firewall: drop RxIn ipv4 tcp frames with unexpected ports (RC_INSPECTA_00-HLR-6) The firewall shall drop any frame from RxIn that is an Ipv4 frame whose protocol is TCP and whose port is not defined in the port whitelist.":
                    (HasEvent(EthernetFramesRxIn) implies
                        '->:'(GumboLib::GUMBO__Library::isIPV4(EthernetFramesRxIn) &
                                GumboLib::GUMBO__Library::isTCP(EthernetFramesRxIn) &
                                (not GumboLib::GUMBO__Library::isPortWhitelisted(EthernetFramesRxIn)),
                            NoSend(EthernetFramesRxOut)));   //  ..or EthernetFramesRxOut != EthernetFramesRxIn

                guarantee RC_INSPECTA_00_HLR_9 "1.9 firewall: copy through allowed tcp port packets (RC_INSPECTA_00-HLR-8; revised CR-01: applies in Normal mode only) In Normal mode, the firewall shall copy any frame from RxIn that is a non-malformed Ipv4 frame with the TCP protocol and whose port is defined in the port whitelist to RxOut.":
                    (HasEvent(EthernetFramesRxIn) implies
                        '->:'(CurrentMode == SW::Mode.Normal &
                                GumboLib::GUMBO__Library::isIPV4(EthernetFramesRxIn) &
                                GumboLib::GUMBO__Library::isTCP(EthernetFramesRxIn) &
                                GumboLib::GUMBO__Library::isPortWhitelisted(EthernetFramesRxIn) &
                                (not GumboLib::GUMBO__Library::isMalformedFrame(EthernetFramesRxIn)),
                            MustSend(EthernetFramesRxOut) and EthernetFramesRxIn == EthernetFramesRxOut));

                guarantee CR01_Rx_ModeGate "FirewallRx_Req_ModeGate (CR-01): in Init and RTL modes, drop every frame — no output regardless of input.":
                    (not (CurrentMode == SW::Mode.Normal))
                        implies NoSend(EthernetFramesRxOut);

                guarantee CR01_Rx_Count "FirewallRx_Req_Count (CR-01): cumulative malformed-frame count since initialization, incremented on each malformed received frame, saturating at 6; mode-independent.":
                    ((HasEvent(EthernetFramesRxIn) and
                      GumboLib::GUMBO__Library::isMalformedFrame(EthernetFramesRxIn) and
                      In(malformedCount) < 6 [i32])
                        implies malformedCount == In(malformedCount) + 1 [i32]) &
                    ((HasEvent(EthernetFramesRxIn) and
                      GumboLib::GUMBO__Library::isMalformedFrame(EthernetFramesRxIn) and
                      In(malformedCount) >= 6 [i32])
                        implies malformedCount == In(malformedCount)) &
                    (((not HasEvent(EthernetFramesRxIn)) or
                      (not GumboLib::GUMBO__Library::isMalformedFrame(EthernetFramesRxIn)))
                        implies malformedCount == In(malformedCount));

                guarantee CR01_Rx_Detect "FirewallRx_Req_Detect (CR-01): report Attack when the (post-update) malformed count exceeds five, OK otherwise.":
                    ((malformedCount > 5 [i32]) implies AttackStatusRx == SW::AttackStatus.Attack) &
                    ((malformedCount <= 5 [i32]) implies AttackStatusRx == SW::AttackStatus.OK);
        }*/
    }

    // -----------------------------------------------------
    //   Thread   T x   F i r e w a l l 
    // -----------------------------------------------------

    part def Firewall_Tx_i :> Periodic_Rust_Thread {
        port EthernetFramesTxIn:  EventDataPort { in :>> type : StructuredEthernetMessage_i; }
        port EthernetFramesTxOut: EventDataPort { out :>> type : StructuredEthernetMessage_i; }

        // CR-01: mode awareness + attack detection (DataPorts per RD-4)
        port CurrentMode:    DataPort { in  :>> type : Mode; }
        port AttackStatusTx: DataPort { out :>> type : AttackStatus; }

        language "GUMBO" /*{
            initialize
                guarantee CR01_Tx_Init "FirewallTx_Req_Init: attack status DataPort initialized to OK.":
                    AttackStatusTx == SW::AttackStatus.OK;

            compute
                guarantee RC_INSPECTA_00_HLR_7 "2.1 firewall: copy out TxIn arp frame (RC_INSPECTA_00-HLR-7; revised CR-01: applies in Normal mode only) In Normal mode, if the firewall gets a wellformed Arp frame from TxIn, the firewall shall copy the frame to TxOut.":
                    (HasEvent(EthernetFramesTxIn) implies
                        '->:'(CurrentMode == SW::Mode.Normal &
                                (not GumboLib::GUMBO__Library::isMalformedFrame(EthernetFramesTxIn)) & GumboLib::GUMBO__Library::isARP(EthernetFramesTxIn),
                            MustSend(EthernetFramesTxOut) and EthernetFramesTxIn == EthernetFramesTxOut));

                guarantee RC_INSPECTA_00_HLR_12 "2.2 firewall: copy out TxIn ipv4 frame (RC_INSPECTA_00-HLR-12; revised CR-01: applies in Normal mode only) In Normal mode, if the firewall gets a wellformed IPv4 frame from TxIn, the firewall shall copy the frame to TxOut.":
                    (HasEvent(EthernetFramesTxIn) implies
                        '->:'(CurrentMode == SW::Mode.Normal &
                                (not GumboLib::GUMBO__Library::isMalformedFrame(EthernetFramesTxIn)) & GumboLib::GUMBO__Library::isIPV4(EthernetFramesTxIn),
                            MustSend(EthernetFramesTxOut) and EthernetFramesTxIn == EthernetFramesTxOut));

                guarantee RC_INSPECTA_00_HLR_14 "2.3 firewall: do not copy disallowed frame (RC_INSPECTA_00-HLR-14) If the firewall gets a malformed ARP frame or malformed TCP frame, it should drop the frame.":
                    (HasEvent(EthernetFramesTxIn) implies
                        '->:'((not GumboLib::GUMBO__Library::isIPV4(EthernetFramesTxIn) and not GumboLib::GUMBO__Library::isARP(EthernetFramesTxIn)) |
                        GumboLib::GUMBO__Library::isMalformedFrame(EthernetFramesTxIn),
                            NoSend(EthernetFramesTxOut)));
                
                guarantee RC_INSPECTA_00_HLR_16 "2.4 firewall: no output on empty input (RC_INSPECTA_00-HLR-16) If the firewall gets no input on TxIn, it should produce no output on TxOut":
                    (not HasEvent(EthernetFramesTxIn) implies
                            NoSend(EthernetFramesTxOut));

                guarantee CR01_Tx_ModeGate "FirewallTx_Req_ModeGate (CR-01): in Init and RTL modes, drop every frame — no output regardless of input.":
                    (not (CurrentMode == SW::Mode.Normal))
                        implies NoSend(EthernetFramesTxOut);

                guarantee CR01_Tx_Detect "FirewallTx_Req_Detect (CR-01): report Attack on any dispatch whose received frame carries the mocked geofence violation (rawMessage byte 0 == 0), OK on every other dispatch; mode-independent, per-dispatch (no latch — persistence is the ModeManager's RTL).":
                    ((HasEvent(EthernetFramesTxIn) and
                      GumboLib::GUMBO__Library::isGeofenceViolation(EthernetFramesTxIn))
                        implies AttackStatusTx == SW::AttackStatus.Attack) &
                    (((not HasEvent(EthernetFramesTxIn)) or
                      (not GumboLib::GUMBO__Library::isGeofenceViolation(EthernetFramesTxIn)))
                        implies AttackStatusTx == SW::AttackStatus.OK);
        }*/
    }

    // -----------------------------------------------------
    //   Thread   A r d u  P i l o t
    // -----------------------------------------------------
    part def ArduPilot_i :> Periodic_Rust_Thread {
        port EthernetFramesRx: EventDataPort { in :>> type : StructuredEthernetMessage_i; }
        port EthernetFramesTx: EventDataPort { out :>> type : StructuredEthernetMessage_i; }
    }

    // -----------------------------------------------------
    //   Thread   M o d e   M a n a g e r   (CR-01)
    // -----------------------------------------------------
    part def ModeManager_i :> Periodic_Rust_Thread {
        port AttackStatusRx: DataPort { in  :>> type : AttackStatus; }
        port AttackStatusTx: DataPort { in  :>> type : AttackStatus; }
        port CurrentMode:    DataPort { out :>> type : Mode; }

        language "GUMBO" /*{
            state
                currentMode: SW::Mode;
                activationCount: Base_Types::Integer_32;

            initialize
                modifies currentMode, activationCount;
                guarantee CR01_MM_Init "ModeManager_Req_Init: start in Init with zero activations; mode DataPort initialized to Init.":
                    currentMode == SW::Mode.Init &
                    activationCount == 0 [i32] &
                    CurrentMode == SW::Mode.Init;

            compute
                modifies currentMode, activationCount;

                guarantee CR01_MM_Count "ModeManager_Req_Count: activation counter increments each dispatch, saturating at 10.":
                    ((In(activationCount) < 10 [i32])
                        implies activationCount == In(activationCount) + 1 [i32]) &
                    ((In(activationCount) >= 10 [i32])
                        implies activationCount == In(activationCount));

                guarantee CR01_MM_Absorbing "ModeManager_Req_Absorbing: RTL is absorbing until restart (RD-3).":
                    (In(currentMode) == SW::Mode.RTL)
                        implies currentMode == SW::Mode.RTL;

                guarantee CR01_MM_ToRTL "ModeManager_Req_ToRTL: when not already in RTL and either firewall reports Attack, enter RTL (wins ties against Init-to-Normal).":
                    ((not (In(currentMode) == SW::Mode.RTL)) &
                     (GumboLib::GUMBO__Library::isAttack(AttackStatusRx) |
                      GumboLib::GUMBO__Library::isAttack(AttackStatusTx)))
                        implies currentMode == SW::Mode.RTL;

                guarantee CR01_MM_StayInit "ModeManager_Req_StayInit: in Init with no attack and (post-increment) count below 10, remain in Init.":
                    ((In(currentMode) == SW::Mode.Init) &
                     (not (GumboLib::GUMBO__Library::isAttack(AttackStatusRx) |
                           GumboLib::GUMBO__Library::isAttack(AttackStatusTx))) &
                     (activationCount < 10 [i32]))
                        implies currentMode == SW::Mode.Init;

                guarantee CR01_MM_ToNormal "ModeManager_Req_ToNormal: in Init with no attack and (post-increment) count reaching 10, transition to Normal.":
                    ((In(currentMode) == SW::Mode.Init) &
                     (not (GumboLib::GUMBO__Library::isAttack(AttackStatusRx) |
                           GumboLib::GUMBO__Library::isAttack(AttackStatusTx))) &
                     (activationCount >= 10 [i32]))
                        implies currentMode == SW::Mode.Normal;

                guarantee CR01_MM_StayNormal "ModeManager_Req_StayNormal: in Normal with no attack, remain in Normal.":
                    ((In(currentMode) == SW::Mode.Normal) &
                     (not (GumboLib::GUMBO__Library::isAttack(AttackStatusRx) |
                           GumboLib::GUMBO__Library::isAttack(AttackStatusTx))))
                        implies currentMode == SW::Mode.Normal;

                guarantee CR01_MM_Broadcast "ModeManager_Req_Broadcast: the mode DataPort output equals the post-transition mode state.":
                    CurrentMode == currentMode;
        }*/
    }

    // ==========================================================================
    //   P r o c e s s e s
    // ==========================================================================

    part def LowLevelEthernetDriver_seL4_i :> Process {
        // Ethernet Frames: Raw Ethernet frames received from the physical network interface.
        port EthernetFramesRx: EventDataPort { out :>> type : StructuredEthernetMessage_i; }
        port EthernetFramesTx: EventDataPort { in :>> type : StructuredEthernetMessage_i; }

        part LowLevelEthernetDriver: LowLevelEthernetDriver_i;

        connection c1: PortConnection connect EthernetFramesTx to LowLevelEthernetDriver.EthernetFramesTx;
        connection c2: PortConnection connect LowLevelEthernetDriver.EthernetFramesRx to EthernetFramesRx;

        attribute :>> Domain = 2;
    }

    // Rx Firewall Process
    part def Firewall_Rx_seL4_i :> Process {
        port EthernetFramesRxIn:  EventDataPort { in :>> type : StructuredEthernetMessage_i; }
        port EthernetFramesRxOut: EventDataPort { out :>> type : StructuredEthernetMessage_i; }

        // CR-01
        port CurrentMode:    DataPort { in  :>> type : Mode; }
        port AttackStatusRx: DataPort { out :>> type : AttackStatus; }

        part FirewallRx: Firewall_Rx_i;


        connection c1: PortConnection connect EthernetFramesRxIn to FirewallRx.EthernetFramesRxIn;
        connection c2: PortConnection connect FirewallRx.EthernetFramesRxOut to EthernetFramesRxOut;

        // CR-01
        connection c3: PortConnection connect CurrentMode to FirewallRx.CurrentMode;
        connection c4: PortConnection connect FirewallRx.AttackStatusRx to AttackStatusRx;

        attribute :>> Domain = 3;
    }

    // Tx Firewall Process
    part def Firewall_Tx_seL4_i :> Process {
        port EthernetFramesTxIn:  EventDataPort { in :>> type : StructuredEthernetMessage_i; }
        port EthernetFramesTxOut: EventDataPort { out :>> type : StructuredEthernetMessage_i; }

        // CR-01
        port CurrentMode:    DataPort { in  :>> type : Mode; }
        port AttackStatusTx: DataPort { out :>> type : AttackStatus; }

        part FirewallTx: Firewall_Tx_i;

        connection c1: PortConnection connect EthernetFramesTxIn to FirewallTx.EthernetFramesTxIn;
        connection c2: PortConnection connect FirewallTx.EthernetFramesTxOut to EthernetFramesTxOut;

        // CR-01
        connection c3: PortConnection connect CurrentMode to FirewallTx.CurrentMode;
        connection c4: PortConnection connect FirewallTx.AttackStatusTx to AttackStatusTx;

        attribute :>> Domain = 4;
    }
    part def ArduPilot_seL4_i :> Process {
        port EthernetFramesRx: EventDataPort { in :>> type : StructuredEthernetMessage_i; }
        port EthernetFramesTx: EventDataPort { out :>> type : StructuredEthernetMessage_i; }

        part ArduPilot: ArduPilot_i;

        connection c1: PortConnection connect EthernetFramesRx to ArduPilot.EthernetFramesRx;
        connection c2: PortConnection connect ArduPilot.EthernetFramesTx to EthernetFramesTx;

        attribute :>> Domain = 5;
    }

    // Mode Manager Process (CR-01)
    part def ModeManager_seL4_i :> Process {
        port AttackStatusRx: DataPort { in  :>> type : AttackStatus; }
        port AttackStatusTx: DataPort { in  :>> type : AttackStatus; }
        port CurrentMode:    DataPort { out :>> type : Mode; }

        part ModeManager: ModeManager_i;

        connection c1: PortConnection connect AttackStatusRx to ModeManager.AttackStatusRx;
        connection c2: PortConnection connect AttackStatusTx to ModeManager.AttackStatusTx;
        connection c3: PortConnection connect ModeManager.CurrentMode to CurrentMode;

        attribute :>> Domain = 6;
    }

    // ==========================================================================
    //   P r o c e s s o r
    // ==========================================================================

    part def ZCU102_Processor :> Processor {
        attribute :>> Frame_Period = 1000[ms];
        attribute :>> Clock_Period = 2[ms];
    }

    // ==========================================================================
    //   T o p - L e v e l    S y s t e m
    // ==========================================================================

    part def seL4_i :> System {
        part proc: ZCU102_Processor;

        part ArduPilot: ArduPilot_seL4_i;
        part FirewallRx: Firewall_Rx_seL4_i;
        part FirewallTx: Firewall_Tx_seL4_i;
        part LowLevelEthernetDriver: LowLevelEthernetDriver_seL4_i;
        part ModeManager: ModeManager_seL4_i;    // CR-01

        // Incoming traffic
        connection c1: PortConnection connect LowLevelEthernetDriver.EthernetFramesRx to FirewallRx.EthernetFramesRxIn;
        connection c2: PortConnection connect FirewallRx.EthernetFramesRxOut to ArduPilot.EthernetFramesRx;
        // Outgoing traffic
        connection c3: PortConnection connect ArduPilot.EthernetFramesTx to FirewallTx.EthernetFramesTxIn;
        connection c4: PortConnection connect FirewallTx.EthernetFramesTxOut to LowLevelEthernetDriver.EthernetFramesTx;
        // CR-01: attack-status feeds and mode broadcast
        connection c5: PortConnection connect FirewallRx.AttackStatusRx to ModeManager.AttackStatusRx;
        connection c6: PortConnection connect FirewallTx.AttackStatusTx to ModeManager.AttackStatusTx;
        connection c7: PortConnection connect ModeManager.CurrentMode to FirewallRx.CurrentMode;
        connection c8: PortConnection connect ModeManager.CurrentMode to FirewallTx.CurrentMode;

        allocation pb0: Deployment_Properties::Actual_Processor_Binding
            allocate ArduPilot to proc;

        allocation pb1: Deployment_Properties::Actual_Processor_Binding
            allocate FirewallRx to proc;

        allocation pb2: Deployment_Properties::Actual_Processor_Binding
            allocate FirewallTx to proc;

        allocation pb3: Deployment_Properties::Actual_Processor_Binding
            allocate LowLevelEthernetDriver to proc;

        allocation pb4: Deployment_Properties::Actual_Processor_Binding
            allocate ModeManager to proc;    // CR-01
    }
}

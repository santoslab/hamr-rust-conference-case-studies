// Status_v2 scenario boundary.
// HAMR code generation intentionally targets GroundStation::GroundStation_Impl
// in GroundStation.sysml, not this containing scenario.

package Status_v2 {

    private import HAMR::*;

    // The HMD's internal hardware/bus hierarchy is outside the component
    // subset currently accepted by HAMR SysML code generation. Its external
    // communication boundary is retained without unsupported model elements.
    part def HMD_Impl :> System {
        port wifiSend: EventDataPort { out :>> type : Common::IncomingWifiMessage_Impl; }
        port wifiRecv: EventDataPort { in :>> type : Common::OutgoingWifiMessage_Impl; }
        port btSend: EventDataPort { out :>> type : Common::DummyMessage_Impl; }
        port btRecv: EventDataPort { in :>> type : Common::DummyMessage_Impl; }
    }

    part def Checkpoint_Impl :> System {
        part groundStation: GroundStation::GroundStation_Impl;
        part hmd: HMD_Impl;

        connection wifi_to_ground_station: PortConnection
            connect hmd.wifiSend to groundStation.wifiRecv;
    }
}

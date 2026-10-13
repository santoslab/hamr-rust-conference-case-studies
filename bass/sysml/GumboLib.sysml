package GumboLib {
    private import HAMR::*;

    language "GUMBO" /*{
        library

        functions
            def isMalformedFrame(v: SW::StructuredEthernetMessage_i): Base_Types::Boolean := v.malformedFrame;

            def getInternetProtocol(v: SW::StructuredEthernetMessage_i): SW::InternetProtocol := v.internetProtocol;
            def isIPV4(v: SW::StructuredEthernetMessage_i): Base_Types::Boolean := getInternetProtocol(v) == SW::InternetProtocol.IPV4;
            def isIPV6(v: SW::StructuredEthernetMessage_i): Base_Types::Boolean := v.internetProtocol == SW::InternetProtocol.IPV6;

            def getFrameProtocol(v: SW::StructuredEthernetMessage_i): SW::FrameProtocol := v.frameProtocol;
            def isTCP(v: SW::StructuredEthernetMessage_i): Base_Types::Boolean := v.frameProtocol == SW::FrameProtocol.TCP;
            def isARP(v: SW::StructuredEthernetMessage_i): Base_Types::Boolean := v.frameProtocol == SW::FrameProtocol.ARP;

            def isPortWhitelisted(v: SW::StructuredEthernetMessage_i): Base_Types::Boolean := v.portIsWhitelisted;

            def getARP_Type(v: SW::StructuredEthernetMessage_i): SW::ARP_Type := v.arpType;
            def isARP_Request(v: SW::StructuredEthernetMessage_i): Base_Types::Boolean := v.arpType == SW::ARP_Type.REQUEST;
            def isARP_Reply(v: SW::StructuredEthernetMessage_i): Base_Types::Boolean := v.arpType == SW::ARP_Type.REPLY;

            // CR-01: mocked geofence-violation indicator (raw byte 0 == 0)
            def isGeofenceViolation(v: SW::StructuredEthernetMessage_i): Base_Types::Boolean := v.rawMessage#(0) == 0 [u8];

            // CR-01: attack-status test
            def isAttack(v: SW::AttackStatus): Base_Types::Boolean := v == SW::AttackStatus.Attack;
    }*/
}

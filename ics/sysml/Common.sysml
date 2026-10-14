package Common {

    private import HAMR::*;

    part def MsgHeader_Impl :> Struct {
        part client: Base_Types::Unsigned_32;
    }

    enum def TargetAssessment {
        enum Unreviewed;
        enum Safe;
        enum Threat;
    }

    part def HMDPosition_Impl :> Struct {
        part positionX: Base_Types::Integer_32;
        part positionY: Base_Types::Integer_32;
        part positionZ: Base_Types::Integer_32;
        part orientationX: Base_Types::Integer_32;
        part orientationY: Base_Types::Integer_32;
        part orientationZ: Base_Types::Integer_32;
        part orientationW: Base_Types::Integer_32;
    }

    part def TargetObservation_Impl :> Struct {
        part targetID: Base_Types::Unsigned_32;
        part locationX: Base_Types::Integer_32;
        part locationY: Base_Types::Integer_32;
        part locationZ: Base_Types::Integer_32;
        attribute assessment: TargetAssessment;
    }

    part def TargetObservationArray_Impl :> Array {
        part :>> Base_Type : TargetObservation_Impl;
        attribute :>> Dimensions = 15;
        attribute :>> Array_Size_Kind = Array_Size_Kinds::Fixed;
        attribute :>> Data_Size = 300 [byte];
    }

    part def Log_Impl :> Struct {
        part timestamp: Base_Types::Unsigned_64;
        part guardID: Base_Types::Unsigned_32;
        part deviceID: Base_Types::Unsigned_32;
        part hmdPosition: HMDPosition_Impl;
        part targetCount: Base_Types::Unsigned_32;
        part targets: TargetObservationArray_Impl;
    }

    enum def AnalysisType {
        enum All_Records;
        enum Threat_Only;
        enum Safe_Only;
        enum Unreviewed_Only;
        enum Target_History;
    }

    part def Request_Impl :> Struct {
        attribute analysisType: AnalysisType;
        part guardID: Base_Types::Unsigned_32;
        part startTime: Base_Types::Unsigned_64;
        part endTime: Base_Types::Unsigned_64;
        part targetID: Base_Types::Unsigned_32;
    }

    part def AnalysisRequest_Impl :> Struct {
        part header: MsgHeader_Impl;
        part payload: Request_Impl;
    }

    part def ResponseLog_Impl :> Array {
        part :>> Base_Type : Log_Impl;
        attribute :>> Dimensions = 10;
        attribute :>> Array_Size_Kind = Array_Size_Kinds::Fixed;
        attribute :>> Data_Size = 3520 [byte];
    }

    part def Response_Impl :> Struct {
        part request: Request_Impl;
        part validLogCount: Base_Types::Unsigned_32;
        part moreAvailable: Base_Types::Boolean;
        part nextStartTime: Base_Types::Unsigned_64;
        part logs: ResponseLog_Impl;
    }

    part def AnalysisResponse_Impl :> Struct {
        part header: MsgHeader_Impl;
        part payload: Response_Impl;
    }

    part def DummyMessage_Impl :> Array {
        part :>> Base_Type : Base_Types::Unsigned_8;
        attribute :>> Dimensions = 100;
        attribute :>> Array_Size_Kind = Array_Size_Kinds::Fixed;
        attribute :>> Data_Size = 100 [byte];
    }

    part def Nonce_Impl :> Array {
        part :>> Base_Type : Base_Types::Unsigned_8;
        attribute :>> Dimensions = 12;
        attribute :>> Array_Size_Kind = Array_Size_Kinds::Fixed;
        attribute :>> Data_Size = 12 [byte];
    }

    part def Ciphertext_Impl :> Array {
        part :>> Base_Type : Base_Types::Unsigned_8;
        attribute :>> Dimensions = 4068;
        attribute :>> Array_Size_Kind = Array_Size_Kinds::Fixed;
        attribute :>> Data_Size = 4068 [byte];
    }

    part def AuthenticationTag_Impl :> Array {
        part :>> Base_Type : Base_Types::Unsigned_8;
        attribute :>> Dimensions = 16;
        attribute :>> Array_Size_Kind = Array_Size_Kinds::Fixed;
        attribute :>> Data_Size = 16 [byte];
    }

    part def EncryptedMessage_Impl :> Struct {
        part nonce: Nonce_Impl;
        part ciphertext: Ciphertext_Impl;
        part tag: AuthenticationTag_Impl;
    }

    part def LogFileMetadata_Impl :> Struct {
        part guardID: Base_Types::Unsigned_32;
        part deviceID: Base_Types::Unsigned_32;
        part timestamp: Base_Types::Unsigned_64;
    }

    part def StoredLogFile_Impl :> Struct {
        part logMetadata: LogFileMetadata_Impl;
        part encryptedLog: EncryptedMessage_Impl;
    }

    part def EncryptedLogArray_Impl :> Array {
        part :>> Base_Type : StoredLogFile_Impl;
        attribute :>> Dimensions = 100;
        attribute :>> Array_Size_Kind = Array_Size_Kinds::Fixed;
        attribute :>> Data_Size = 411200 [byte];
    }

    part def EncryptedResponseLog_Impl :> Array {
        part :>> Base_Type : StoredLogFile_Impl;
        attribute :>> Dimensions = 10;
        attribute :>> Array_Size_Kind = Array_Size_Kinds::Fixed;
        attribute :>> Data_Size = 41120 [byte];
    }

    part def EncryptedResponse_Impl :> Struct {
        part request: Request_Impl;
        part validLogCount: Base_Types::Unsigned_32;
        part moreAvailable: Base_Types::Boolean;
        part nextStartTime: Base_Types::Unsigned_64;
        part logs: EncryptedResponseLog_Impl;
    }

    part def EncryptedAnalysisResponse_Impl :> Struct {
        part header: MsgHeader_Impl;
        part payload: EncryptedResponse_Impl;
    }

    part def shortText :> Array {
        part :>> Base_Type : Base_Types::Character;
        attribute :>> Dimensions = 64;
        attribute :>> Array_Size_Kind = Array_Size_Kinds::Fixed;
        attribute :>> Data_Size = 64 [byte];
    }

    part def IncomingWifiHeader_Impl :> Struct {
        part route: shortText;
        part client: Base_Types::Unsigned_32;
    }

    part def IncomingWifiMessage_Impl :> Struct {
        part header: IncomingWifiHeader_Impl;
        part payload: EncryptedMessage_Impl;
    }

    part def OutgoingWifiMessage_Impl :> Struct {
        part header: MsgHeader_Impl;
        part payload: EncryptedMessage_Impl;
    }
}

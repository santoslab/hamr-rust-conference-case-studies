package MATRICS_Model_Transformations {

    language "GUMBO" /*{
        library
            functions
                def FOUND_IN_ALLOW_LIST(
                    src: Base_Types::Unsigned_32): Base_Types::Boolean :=
                    src == 3232235877 [u32] or
                    src == 3232235878 [u32] or
                    src == 3232235879 [u32] or
                    src == 3232235880 [u32];

                def AES_128_GCM_DECRYPTS_LOG(
                    encrypted_message: Common::EncryptedMessage_Impl,
                    decrypted: Common::Log_Impl): Base_Types::Boolean;

                def AES_128_GCM_ENCRYPTS_RESPONSE(
                    response: Common::Response_Impl,
                    encrypted: Common::EncryptedMessage_Impl): Base_Types::Boolean;

                def IS_NULL_HMD_POSITION(
                    position: Common::HMDPosition_Impl): Base_Types::Boolean :=
                    position.positionX == 0 [i32] &
                    position.positionY == 0 [i32] &
                    position.positionZ == 0 [i32] &
                    position.orientationX == 0 [i32] &
                    position.orientationY == 0 [i32] &
                    position.orientationZ == 0 [i32] &
                    position.orientationW == 0 [i32];

                def IS_NULL_TARGET(
                    target: Common::TargetObservation_Impl): Base_Types::Boolean :=
                    target.targetID == 0 [u32] &
                    target.locationX == 0 [i32] &
                    target.locationY == 0 [i32] &
                    target.locationZ == 0 [i32] &
                    target.assessment == Common::TargetAssessment.Unreviewed;

                def IS_NULL_LOG(
                    log: Common::Log_Impl): Base_Types::Boolean :=
                    log.timestamp == 0 [u64] &
                    log.guardID == 0 [u32] &
                    log.deviceID == 0 [u32] &
                    IS_NULL_HMD_POSITION(log.hmdPosition) &
                    log.targetCount == 0 [u32] &
                    ((0 .. size(log.targets) - 1) -> forAll { in target_index;
                        IS_NULL_TARGET(log.targets#(target_index))
                    });

                def IS_NULL_REQUEST(
                    request: Common::Request_Impl): Base_Types::Boolean :=
                    request.analysisType == Common::AnalysisType.All_Records &
                    request.guardID == 0 [u32] &
                    request.startTime == 0 [u64] &
                    request.endTime == 0 [u64] &
                    request.targetID == 0 [u32];

    }*/
}

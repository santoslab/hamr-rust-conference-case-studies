FROM jasonbelt/microkit_provers:2026.10.13

RUN echo "ARM: Install Custom LionsOS" && \
  cd ${PROVERS_DIR} && \
  rm -rf lionsos && \
  git clone --rec --depth=1 --shallow-submodules https://github.com/aaurandt/lionsos.git ${LIONSOS} && \
  rm -rf ${PROVERS_DIR}/lionsos/dep/micropython ${PROVERS_DIR}/lionsos/dep/wasm-micro-runtime \
    ${PROVERS_DIR}/lionsos/examples ${PROVERS_DIR}/lionsos/.git \
    ${PROVERS_DIR}/*tar.gz ${PROVERS_DIR}/zig* ${PROVERS_DIR}/microkit_sdf_gen

WORKDIR /home/microkit/ICS

RUN sudo apt-get update -y && sudo apt install cpio vim -y

EXPOSE 8080/tcp
EXPOSE 8443/tcp
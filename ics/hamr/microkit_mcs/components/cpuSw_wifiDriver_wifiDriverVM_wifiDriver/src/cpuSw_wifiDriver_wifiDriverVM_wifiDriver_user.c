#include <cpuSw_wifiDriver_wifiDriverVM_wifiDriver.h>
#include <cpuSw_wifiDriver_wifiDriverVM_wifiDriver_user.h>
#include <libvmm/guest.h>
#include <libvmm/guest_ram.h>
#include <libvmm/virq.h>
#include <libvmm/util/util.h>
#include <libvmm/arch/aarch64/linux.h>
#include <libvmm/arch/aarch64/fault.h>
#include <string.h>
#include <stdlib.h>

// This file will not be overwritten if HAMR codegen is rerun

// Data for the guest's kernel image.
extern char _guest_kernel_image[];
extern char _guest_kernel_image_end[];

// Data for the device tree to be passed to the kernel.
extern char _guest_dtb_image[];
extern char _guest_dtb_image_end[];

// Data for the initial RAM disk to be passed to the kernel.
extern char _guest_initrd_image[];
extern char _guest_initrd_image_end[];

// Microkit will set this variable to the start of the guest RAM memory region.
uintptr_t GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_Guest_RAM_vaddr;

// Microkit will set this variable to the start of the RX memory buffer
uintptr_t GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_Guest_RX_Buffer_vaddr;

// Microkit will set this variable to the start of the TX memory buffer
uintptr_t GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_Guest_TX_Buffer_vaddr;

static bool is_passthrough_irq_ch(microkit_channel ch);
static bool parse_message(const char* str, Common_IncomingWifiMessage_Impl *message);

void cpuSw_wifiDriver_wifiDriverVM_wifiDriver_initialize(void) {
  // Initialise the VMM, the VCPU(s), and start the guest
  LOG_VMM("starting \"%s\"\n", microkit_name);

  // Declare the guest's RAM layout before anything else. guest_init brings up
  // the architectural subsystems everything below depends on, in particular the
  // virtual GIC, and registers the RAM regions that guest physical addresses are
  // resolved against.
  arch_guest_init_t guest_args = {
    .pci_init.mmio_aperature_size = 0, // no virtual PCI bus
    .num_vcpus = 1,
    .num_guest_ram_regions = 1,
    .guest_ram_regions = { (struct guest_ram_region) {
      .gpa_start = GUEST_RAM_START_VADDR,
      .size = GUEST_RAM_SIZE,
      .vmm_vaddr = (void *) GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_Guest_RAM_vaddr } }
  };

  bool success = guest_init(guest_args);
  if (!success) {
    LOG_VMM_ERR("Failed to initialise guest\n");
    return;
  }

  // Place all the binaries in the right locations before starting the guest

  size_t kernel_size = _guest_kernel_image_end - _guest_kernel_image;
  size_t dtb_size = _guest_dtb_image_end - _guest_dtb_image;
  size_t initrd_size = _guest_initrd_image_end - _guest_initrd_image;

  uintptr_t kernel_pc = linux_setup_images(GUEST_RAM_START_VADDR,
                                          (uintptr_t) _guest_kernel_image,
                                          kernel_size,
                                          (uintptr_t) _guest_dtb_image,
                                          GUEST_DTB_VADDR,
                                          dtb_size,
                                          (uintptr_t) _guest_initrd_image,
                                          GUEST_INIT_RAM_DISK_VADDR,
                                          initrd_size);

  if (!kernel_pc) {
    LOG_VMM_ERR("Failed to initialise guest images\n");
    return;
  }

  // Register the pass-through device IRQs. libvmm acks the hardware IRQ itself
  // once the guest acks the virtual one, so no ack handler is needed here.
  for(int i=0; i < MAX_IRQS; i++) {
    success = virq_register_passthrough(ARM_GIC_IRQ_ROUTE(GUEST_BOOT_VCPU_ID, mk_irqs[i].irq), mk_irqs[i].channel);
    if (!success) {
      LOG_VMM_ERR("Failed to register pass-through IRQ %d\n", mk_irqs[i].irq);
      return;
    }
    // Just in case there are already interrupts available to handle, we ack them here.
    microkit_irq_ack(mk_irqs[i].channel);
  }

  // Finally start the guest
  success = guest_start(kernel_pc, GUEST_DTB_VADDR, GUEST_INIT_RAM_DISK_VADDR);
  if (!success) {
    LOG_VMM_ERR("Failed to start guest\n");
    return;
  }

  LOG_VMM("Guest started, leaving cpuSw_wifiDriver_wifiDriverVM_wifiDriver_initialize\n");
}

void cpuSw_wifiDriver_wifiDriverVM_wifiDriver_timeTriggered(void) {
     uint32_t rx_ready = *(uint32_t *)GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_Guest_RX_Buffer_vaddr;
     if (rx_ready == 1){
          Common_IncomingWifiMessage_Impl message;
          char *data = (char *)(GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_Guest_RX_Buffer_vaddr + 0x04);
          if (parse_message(data, &message)){
               if (put_wifiRecvOut(&message)){
                    // Reset RX flag
                    *(uint32_t *)GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_Guest_RX_Buffer_vaddr = 0;
               }
          } else { // Message is not of correct format
               // Reset RX flag
               *(uint32_t *)GroundStation_Impl_Instance_cpuSw_wifiDriver_wifiDriverVM_wifiDriver_VM_Guest_RX_Buffer_vaddr = 0;
          }
     }
}

void cpuSw_wifiDriver_wifiDriverVM_wifiDriver_notify(microkit_channel ch) {
  if (is_passthrough_irq_ch(ch)) {
    if (!virq_handle_passthrough(ch)) {
      LOG_VMM_ERR("IRQ dropped on channel 0x%x\n", ch);
    }
    return;
  }

  printf("Unexpected channel, ch: 0x%x\n", ch);
}

/*
 * The primary purpose of the VMM after initialisation is to act as a fault-handler.
 * Whenever our guest causes an exception, it gets delivered to this entry point for
 * the VMM to handle.
 */
seL4_Bool fault(microkit_child child, microkit_msginfo msginfo, microkit_msginfo *reply_msginfo) {
    bool success = fault_handle(child, msginfo);
    if (success) {
        // Now that we have handled the fault successfully, we reply to it so
        // that the guest can resume execution.
        *reply_msginfo = microkit_msginfo_new(0, 0);
        return seL4_True;
    }

    return seL4_False;
}

static bool is_passthrough_irq_ch(microkit_channel ch) {
  for(int i=0; i < MAX_IRQS; i++) {
    if (mk_irqs[i].channel == ch) {
      return true;
    }
  }


  return false;
}

// Reverse lookup table mapping ASCII characters to 6-bit values
static const int b64_index[256] = {
    ['A'] = 0,  ['B'] = 1,  ['C'] = 2,  ['D'] = 3,  ['E'] = 4,  ['F'] = 5,
    ['G'] = 6,  ['H'] = 7,  ['I'] = 8,  ['J'] = 9,  ['K'] = 10, ['L'] = 11,
    ['M'] = 12, ['N'] = 13, ['O'] = 14, ['P'] = 15, ['Q'] = 16, ['R'] = 17,
    ['S'] = 18, ['T'] = 19, ['U'] = 20, ['V'] = 21, ['W'] = 22, ['X'] = 23,
    ['Y'] = 24, ['Z'] = 25, ['a'] = 26, ['b'] = 27, ['c'] = 28, ['d'] = 29,
    ['e'] = 30, ['f'] = 31, ['g'] = 32, ['h'] = 33, ['i'] = 34, ['j'] = 35,
    ['k'] = 36, ['l'] = 37, ['m'] = 38, ['n'] = 39, ['o'] = 40, ['p'] = 41,
    ['q'] = 42, ['r'] = 43, ['s'] = 44, ['t'] = 45, ['u'] = 46, ['v'] = 47,
    ['w'] = 48, ['x'] = 49, ['y'] = 50, ['z'] = 51, ['0'] = 52, ['1'] = 53,
    ['2'] = 54, ['3'] = 55, ['4'] = 56, ['5'] = 57, ['6'] = 58, ['7'] = 59,
    ['8'] = 60, ['9'] = 61, ['+'] = 62, ['/'] = 63, ['='] = 0
};

// Decodes a base64 string and returns the length of decoded data.
size_t base64_decode(const char *src, uint8_t *dst) {
    size_t len = strlen(src);
    if (len == 0 || len % 4 != 0) return 0; // Base64 strings must be a multiple of 4

    size_t out_len = (len / 4) * 3;
    
    // Adjust output size based on trailing padding characters
    if (src[len - 1] == '=') out_len--;
    if (src[len - 2] == '=') out_len--;

    size_t i, j;
    for (i = 0, j = 0; i < len; i += 4, j += 3) {
        // Pack 4 6-bit values into a 24-bit buffer
        uint32_t sextet_a = b64_index[(unsigned char)src[i]];
        uint32_t sextet_b = b64_index[(unsigned char)src[i+1]];
        uint32_t sextet_c = b64_index[(unsigned char)src[i+2]];
        uint32_t sextet_d = b64_index[(unsigned char)src[i+3]];

        uint32_t triple = (sextet_a << 18) | (sextet_b << 12) | (sextet_c << 6) | sextet_d;

        // Unpack into 3 bytes
        if (j < out_len)     dst[j]   = (triple >> 16) & 0xFF;
        if (j + 1 < out_len) dst[j+1] = (triple >> 8) & 0xFF;
        if (j + 2 < out_len) dst[j+2] = triple & 0xFF;
    }

    return out_len;
}


uint32_t string_to_ip(const char** str){
     uint32_t ip = 0;
     char value[4];
     size_t i;
     for (int j = 24; j >= 0; j=j-8){
          i = 0;
          while(**str != '.' && i < 3){
               value[i++] = **str;
               (*str)++;
          }
          if(**str == '.'){
               (*str)++; // skip dot
          }
          value[i] = '\0'; // Null-terminate the string
          ip = ip | ((uint32_t)atoi(value) << j);
     }
     return ip;
} 

void skip_whitespace(const char **str) {
     while(**str == ' '){
          (*str)++;
     }
}

void parse_string(const char **str, char *dest, size_t dest_size){
     (*str)++; // Skip openning quote
     size_t i = 0;

     while (**str != '"' && **str != '\0'){
          if (i < dest_size){
               dest[i++] = **str;
          }
          (*str)++;
     }

     dest[i] = '\0'; // Null-terminate the string

     if(**str == '"')
          (*str)++; // Skip ending quote
}

void parse_string_first_item(const char **str, char *dest, size_t dest_size){
     (*str)++; // Skip openning quote
     size_t i = 0;

     while (**str != '"' && **str != '\0' && **str != ','){
          if (i < dest_size){
               dest[i++] = **str;
          }
          (*str)++;
     }
     
     dest[i] = '\0'; // Null-terminate the string

     while (**str != '"' && **str != '\0'){ // Ignore rest of list
          (*str)++;
     }

     if(**str == '"')
          (*str)++; // Skip ending quote
}

static bool parse_message(const char* str, Common_IncomingWifiMessage_Impl *message){
     Common_IncomingWifiHeader_Impl header;
     skip_whitespace(&str);
     if(*str != '{'){
          return false; // Invalid JSON
     }
     str++; // Skip '{'

     while(1) {
          skip_whitespace(&str);
          if (*str == '}'){
               str++; // Skip '}'
               break;
          }

          // Parse key
          char key[64];
          parse_string(&str, key, sizeof(key));
          skip_whitespace(&str);
          if (*str != ':'){
               return false; // Invalid JSON
          }
          str++; // Skip ':'
          skip_whitespace(&str);
          if(strcmp(key, "headers") == 0){
               if(*str != '{'){
                    return false; // Invalid JSON
               }
               str++; // Skip '{'
               while(1){
                    skip_whitespace(&str);
                    if (*str == '}'){
                         str++; // Skip '}'
                         break;
                    }
                    // Parse key
                    char header_key[64];
                    parse_string(&str, header_key, sizeof(header_key));
                    skip_whitespace(&str);
                    if (*str != ':'){
                         return false; // Invalid JSON
                    }
                    str++; // Skip ':'
                    skip_whitespace(&str);
                    char value[64];
                    if(strcmp(header_key, "Host") == 0){
                         parse_string(&str, value, sizeof(value));
                         strcpy(header.route, value);
                    } else if(strcmp(header_key, "X-Forwarded-For") == 0){
                         parse_string_first_item(&str, value, sizeof(value));
                         const char *temp_ptr = value;
                         header.client = string_to_ip(&temp_ptr);
                    }
                    else {
                         parse_string(&str, value, sizeof(value));
                    }
                    skip_whitespace(&str);
                    if (*str == ','){
                         str++;
                         skip_whitespace(&str);
                    }
               }
          } else if(strcmp(key, "body") == 0){
               char encoded[5464]; // 4096 of decoded message is represented in 5464 base64 bytes
               parse_string(&str, encoded, sizeof(encoded));
               uint8_t decoded[4096]; // 12-byte nonce + 4068-byte ciphertext + 16-byte tag = 4096 bytes
               size_t length = base64_decode(encoded, decoded);
               memcpy((char*)(*message).payload.nonce, decoded, 12); // Nonce/Initialization Vector(IV) first 12 bytes
               size_t ciphertext_length = length - 12 - 16;
               memcpy((char*)(*message).payload.ciphertext, decoded + 12, ciphertext_length); // Cyphertext
               message->payload.ciphertext[ciphertext_length] = '\0'; // Null-byte terminate
               memcpy((char*)(*message).payload.tag, decoded + 12 + ciphertext_length, 16); // Tag/Checksum last 16 bytes
          } else {
               return false; // Unexpected JSON member
          }
          if (*str == ','){ // More members
               str++; // Skip ','
               skip_whitespace(&str);
          }
     }
     (*message).header = header;
     return true;
}

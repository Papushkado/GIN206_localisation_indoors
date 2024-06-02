#include "contiki.h"
#include "net/rime/rime.h"
#include <stdio.h>
#include <string.h>

#include "sys/node-id.h"
#include "dev/radio-sensor.h"

/*---------------------------------------------------------------------------*/
PROCESS(localizor_process, "Node helping localize");
AUTOSTART_PROCESSES(&localizor_process);
/*---------------------------------------------------------------------------*/
const char* init_msg = "Initial";
const char* request_msg = "Request";
const char* response_msg = "Respons"; // Typo intentional. All messages must
// have the same size. This is a hacky way to make the function below work.
static int request_msg_length, response_msg_length;
static linkaddr_t addr_node_to_localize, addr2;
/*---------------------------------------------------------------------------*/

static void recv_init_uc(struct unicast_conn *c, const linkaddr_t *from) {
  request_msg_length = strlen(request_msg);
  response_msg_length = strlen(response_msg);
  char* payload = (char *)packetbuf_dataptr();

  if (!strcmp(payload, init_msg)) {
    addr_node_to_localize = *from;
    packetbuf_copyfrom(request_msg, request_msg_length);
    unicast_send(c, &addr2);
  } else {
    if (!strcmp(payload, request_msg)) {
      packetbuf_copyfrom(response_msg, response_msg_length);
      unicast_send(c, from);
    } else {
      if (!strcmp(payload, response_msg)) {
        int rssi = radio_sensor.value(RADIO_SENSOR_LAST_VALUE);
        char str_rssi[7];
        sprintf(str_rssi, "%d", rssi);

        packetbuf_copyfrom(str_rssi, strlen(str_rssi));
        unicast_send(c, &addr_node_to_localize);
      }
    }
  }
}
static void sent_init_uc(struct unicast_conn *c, int status, int num_tx) {}

/*---------------------------------------------------------------------------*/
static const struct unicast_callbacks init_unicast_callbacks = {recv_init_uc, sent_init_uc};
static struct unicast_conn init_uc;

/*---------------------------------------------------------------------------*/
PROCESS_THREAD(localizor_process, ev, data)
{
  PROCESS_EXITHANDLER(unicast_close(&init_uc););
    
  addr2.u8[1] = 0;
  addr2.u8[0] = 3;

  PROCESS_BEGIN();

  unsigned short new_node_id = 123;
  node_id_burn(new_node_id);

  SENSORS_ACTIVATE(radio_sensor);
  unicast_open(&init_uc, 146, &init_unicast_callbacks);

  PROCESS_WAIT_EVENT_UNTIL(0);

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/

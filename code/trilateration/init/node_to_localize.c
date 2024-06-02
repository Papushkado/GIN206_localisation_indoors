#include "contiki.h"
#include "net/rime/rime.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "sys/node-id.h"
#include "dev/radio-sensor.h"

#define INITIALISATION_PAYLOAD "Initial"
#define INITIALISATION_INTERVAL CLOCK_SECOND

/*---------------------------------------------------------------------------*/
PROCESS(node_to_localized_process, "Node to localize");
AUTOSTART_PROCESSES(&node_to_localized_process);
/*---------------------------------------------------------------------------*/
static void recv_init_uc(struct unicast_conn *c, const linkaddr_t *from) {
  char* payload = (char *)packetbuf_dataptr();
  printf("Init from %d.%d: %d\n", from->u8[0], from->u8[1], atoi(payload));
  if (from->u8[0] == 4 && from->u8[1] == 0) {
    printf("Done\n");
  }
}
static void sent_init_uc(struct unicast_conn *c, int status, int num_tx) {}

/*---------------------------------------------------------------------------*/
static const struct unicast_callbacks init_unicast_callbacks = {recv_init_uc, sent_init_uc};
static struct unicast_conn init_uc;
static linkaddr_t addr1, addr2, addr3;

static struct etimer et;
/*---------------------------------------------------------------------------*/
PROCESS_THREAD(node_to_localized_process, ev, data)
{
  PROCESS_EXITHANDLER(unicast_close(&init_uc););

  PROCESS_BEGIN();

  unsigned short new_node_id = 321;
  node_id_burn(new_node_id);

  SENSORS_ACTIVATE(radio_sensor);

  addr1.u8[1] = 0;
  addr1.u8[0] = 2;
  addr2.u8[1] = 0;
  addr2.u8[0] = 3;
  addr3.u8[1] = 0;
  addr3.u8[0] = 4;

  const char* init_msg = INITIALISATION_PAYLOAD;
  int init_msg_length = strlen(init_msg);

  unicast_open(&init_uc, 146, &init_unicast_callbacks);

  while (1) {
    packetbuf_copyfrom(init_msg, init_msg_length);
    unicast_send(&init_uc, &addr1);
    etimer_set(&et, INITIALISATION_INTERVAL);
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&et));

    packetbuf_copyfrom(init_msg, init_msg_length);
    unicast_send(&init_uc, &addr2);
    etimer_set(&et, INITIALISATION_INTERVAL);
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&et));

    packetbuf_copyfrom(init_msg, init_msg_length);
    unicast_send(&init_uc, &addr3);
    etimer_set(&et, INITIALISATION_INTERVAL);
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&et));
  }

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/

#include "contiki.h"
#include "net/rime/rime.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "sys/node-id.h"
#include "dev/radio-sensor.h"

#define RETREIVE_ALL_RSSI_INTERVAL (3 * CLOCK_SECOND)
#define ASK_RSSI_INTERVAL (CLOCK_SECOND / 4)

/*---------------------------------------------------------------------------*/
PROCESS(node_to_localized_process, "Node to localize");
AUTOSTART_PROCESSES(&node_to_localized_process);
/*---------------------------------------------------------------------------*/

static void recv_main_uc(struct unicast_conn *c, const linkaddr_t *from) {
  printf("%d.%d: %d\n", from->u8[0], from->u8[1], radio_sensor.value(RADIO_SENSOR_LAST_VALUE));
  if (from->u8[0] == 4 && from->u8[1] == 0) {
    printf("Done\n");
  }
}
static void sent_main_uc(struct unicast_conn *c, int status, int num_tx) {}
/*---------------------------------------------------------------------------*/
static const struct unicast_callbacks main_unicast_callbacks = {recv_main_uc, sent_main_uc};
static struct unicast_conn main_uc;
static linkaddr_t addr1, addr2, addr3;

static struct etimer et;
/*---------------------------------------------------------------------------*/
PROCESS_THREAD(node_to_localized_process, ev, data)
{
  PROCESS_EXITHANDLER(unicast_close(&main_uc););

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

  unicast_open(&main_uc, 146, &main_unicast_callbacks);

  while (1) {
    etimer_set(&et, RETREIVE_ALL_RSSI_INTERVAL);
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&et));

    unicast_send(&main_uc, &addr1);

    etimer_set(&et, ASK_RSSI_INTERVAL);
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&et));

    unicast_send(&main_uc, &addr2);

    etimer_set(&et, ASK_RSSI_INTERVAL);
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&et));

    unicast_send(&main_uc, &addr3);
  }

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/

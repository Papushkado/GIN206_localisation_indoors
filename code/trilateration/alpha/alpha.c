#include "contiki.h"
#include "net/rime/rime.h"
#include <stdio.h>
#include <string.h>

#include "sys/node-id.h"
#include "dev/button-sensor.h"
#include "dev/radio-sensor.h"

#define INITIALISATION_INTERVAL 2 * CLOCK_SECOND

/*---------------------------------------------------------------------------*/
PROCESS(alpha_process, "Alpha");
AUTOSTART_PROCESSES(&alpha_process);
/*---------------------------------------------------------------------------*/
static void recv_init_unicast(struct unicast_conn *c, const linkaddr_t *from) {
  int rssi = radio_sensor.value(RADIO_SENSOR_LAST_VALUE);
  printf("Init from %d.%d: %d\n", from->u8[0], from->u8[1], rssi);
}

/*---------------------------------------------------------------------------*/
static const struct unicast_callbacks init_unicast_callbacks = {recv_init_unicast};
static struct unicast_conn init_unicast;
static linkaddr_t addr_helper;

static struct etimer et;
/*---------------------------------------------------------------------------*/
PROCESS_THREAD(alpha_process, ev, data)
{
  PROCESS_EXITHANDLER(unicast_close(&init_unicast););

  PROCESS_BEGIN();

  unsigned short new_node_id = 321;
  node_id_burn(new_node_id);

  SENSORS_ACTIVATE(radio_sensor);

  addr_helper.u8[1] = 0;
  addr_helper.u8[0] = 2;
  
  SENSORS_ACTIVATE(button_sensor);
  SENSORS_ACTIVATE(radio_sensor);
  printf("Waiting for you to press the button\n");
  PROCESS_WAIT_EVENT_UNTIL(ev == sensors_event && data == &button_sensor);

  printf("Starting Initialisation\n");
  unicast_open(&init_unicast, 146, &init_unicast_callbacks);

  while (1) {
    etimer_set(&et, INITIALISATION_INTERVAL);
    PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&et));

    unicast_send(&init_unicast, &addr_helper);
  }

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/

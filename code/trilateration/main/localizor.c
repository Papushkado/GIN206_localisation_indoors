#include "contiki.h"
#include "net/rime/rime.h"
#include <stdio.h>
#include <string.h>

#include "sys/node-id.h"

/*---------------------------------------------------------------------------*/
PROCESS(localizor_process, "Node helping localize");
AUTOSTART_PROCESSES(&localizor_process);

/*---------------------------------------------------------------------------*/
static void recv_main_uc(struct unicast_conn *c, const linkaddr_t *from) {
  unicast_send(c, from);
}
static void sent_main_uc(struct unicast_conn *c, int status, int num_tx) {}

/*---------------------------------------------------------------------------*/
static const struct unicast_callbacks main_unicast_callbacks = {recv_main_uc, sent_main_uc};
static struct unicast_conn main_uc;

/*---------------------------------------------------------------------------*/
PROCESS_THREAD(localizor_process, ev, data)
{
  PROCESS_EXITHANDLER(unicast_close(&main_uc););
    
  PROCESS_BEGIN();

  unsigned short new_node_id = 123;
  node_id_burn(new_node_id);

  unicast_open(&main_uc, 146, &main_unicast_callbacks);

  PROCESS_WAIT_EVENT_UNTIL(0);

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/

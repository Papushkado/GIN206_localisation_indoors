#include "contiki.h"
#include "net/rime/rime.h"
#include <stdio.h>
#include <string.h>

#include "sys/node-id.h"

/*---------------------------------------------------------------------------*/
PROCESS(helper_process, "Helper node");
AUTOSTART_PROCESSES(&helper_process);

/*---------------------------------------------------------------------------*/
static void recv_init_unicast(struct unicast_conn *c, const linkaddr_t *from) {
  unicast_send(c, from);
}

/*---------------------------------------------------------------------------*/
static const struct unicast_callbacks init_unicast_callbacks = {recv_init_unicast};
static struct unicast_conn init_unicast;

/*---------------------------------------------------------------------------*/
PROCESS_THREAD(helper_process, ev, data)
{
  PROCESS_EXITHANDLER(unicast_close(&init_unicast););

  PROCESS_BEGIN();

  unsigned short new_node_id = 123;
  node_id_burn(new_node_id);

  unicast_open(&init_unicast, 146, &init_unicast_callbacks);

  PROCESS_WAIT_EVENT_UNTIL(0);

  PROCESS_END();
}
/*---------------------------------------------------------------------------*/

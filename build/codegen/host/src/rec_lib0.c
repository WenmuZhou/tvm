#include "tvm/runtime/c_runtime_api.h"
#ifdef __cplusplus
extern "C" {
#endif
__attribute__((section(".data.tvm"), aligned(16)))
static uint8_t global_workspace[1868768];
#include <tvmgen_rec.h>
TVM_DLL int32_t tvmgen_rec___tvm_main__(void* x,void* output0,uint8_t* global_workspace_0_var);
int32_t tvmgen_rec_run(struct tvmgen_rec_inputs* inputs,struct tvmgen_rec_outputs* outputs) {return tvmgen_rec___tvm_main__(inputs->x,outputs->output,&global_workspace);
}
#ifdef __cplusplus
}
#endif
;
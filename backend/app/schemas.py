from pydantic import BaseModel, Field

class WorkerRegisterRequest(BaseModel):
    worker_id: str = Field(..., description="Unique worker id")
    host: str = Field(..., description="Worker host")
    total_cpu: int = Field(..., gt=0, description="Total CPU cores")
    total_mem: int = Field(..., gt=0, description="Total memory in GB")


class TaskCreateRequest(BaseModel):
    command: str = Field(..., min_length=1, description="Command to run")
    cpu_required: int = Field(..., gt=0, description="Required CPU cores")
    mem_required: int = Field(..., gt=0, description="Required memory in GB")


class WorkerHeartbeatRequest(BaseModel):
    worker_id: str
    used_cpu: int = Field(..., ge=0)
    used_mem: int = Field(..., ge=0)
    running_tasks: list[str] = Field(default_factory=list)
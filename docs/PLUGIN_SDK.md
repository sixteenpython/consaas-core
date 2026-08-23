# Plugin SDK

## Design

The SDK is a small, stable package containing protocols and value types—not orchestration or domain implementations. Plugins register a descriptor containing `plugin_id`, semantic version, plugin type, supported SDK range, input/output schema IDs, capabilities, side effects, configuration schema, and factory entry point.

```python
class DataConnector(Protocol):
    def discover(self, request: AcquisitionRequest, ctx: RunContext) -> SourcePlan: ...
    def acquire(self, plan: SourcePlan, ctx: RunContext) -> Artifact[SourceSnapshot]: ...
    def validate(self, artifact: Artifact[SourceSnapshot], ctx: RunContext) -> ValidationResult: ...


class GoldenAssetBuilder(Protocol):
    def build(self, sources: Sequence[Artifact], ctx: RunContext) -> Artifact[GoldenAsset]: ...


class Distiller(Protocol):
    def distill(
        self, asset: Artifact[GoldenAsset], request: DecisionRequest, ctx: RunContext
    ) -> Artifact[DecisionView]: ...


class DecisionEngine(Protocol):
    def decide(
        self, view: Artifact[DecisionView], request: DecisionRequest, ctx: RunContext
    ) -> Artifact[DecisionResult]: ...


class RecommendationGenerator(Protocol):
    def recommend(
        self, result: Artifact[DecisionResult], context: RecommendationContext, ctx: RunContext
    ) -> Artifact[RecommendationSet]: ...


class ReportGenerator(Protocol):
    def compose(
        self,
        recommendations: Artifact[RecommendationSet],
        evidence: EvidenceResolver,
        ctx: RunContext,
    ) -> Artifact[ReportBundle]: ...


class DashboardProvider(Protocol):
    def pages(self, report: Artifact[ReportBundle], ctx: ServingContext) -> Sequence[PageSpec]: ...
```

`Artifact[T]` is immutable and combines a standard envelope with a validated payload. `EvidenceResolver` can resolve only artifacts in the release lineage. `RunContext` offers clock, logger, metrics, artifact writer, scoped secrets, cache, and cancellation; plugins do not instantiate infrastructure clients directly.

## Recommendation contract

Each recommendation includes subject, action code, direction, priority, magnitude/unit, effective and expiry times, confidence with calibration method, structured reason codes, evidence references, assumptions, risks, alternatives, explanation tokens, policy result, and optional execution instructions. Narrative is derived from these fields.

## Dashboard contract

`PageSpec` is channel-neutral: sections contain metric, prose, table, chart, action, evidence, disclosure, and extension blocks. Core supplies renderers and a standard shell. Product extensions are sandboxed blocks; arbitrary UI code is the exception.

## Compatibility and conformance

- Semantic SDK version and declared compatibility range.
- JSON Schema/Pydantic-compatible schemas with stable IDs.
- Contract tests supplied by Core for every plugin type.
- Required golden fixtures, idempotency tests, error taxonomy, and provenance assertions.
- Deprecated fields follow a documented window; breaking changes require a new major contract.
- Plugins declare deterministic, seeded, snapshot-replayable, or non-replayable reproducibility class.

## Failure and LLM rules

Plugins return typed outcomes: success, degraded, needs-review, rejected, retryable failure, or terminal failure. LLM plugins must use structured output, record provider/model/prompt/template/tool versions, set timeout and token budgets, validate citations/evidence, and define a declared fallback. LLM prose cannot override numeric or policy results.

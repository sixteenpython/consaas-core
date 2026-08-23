# ruff: noqa: E501
"""Skill-backed deterministic blueprints used with or without a local model."""

from __future__ import annotations

from dataclasses import dataclass

from narrative_architect.knowledge.nka import NarrativeState

BOOKER_PLOTS = (
    "Overcoming the Monster",
    "Rags to Riches",
    "The Quest",
    "Voyage and Return",
    "Comedy",
    "Tragedy",
    "Rebirth",
)
STRUCTURES = (
    "Three Act",
    "Freytag's Pyramid",
    "Seven Point Story",
    "Save the Cat",
    "Non-linear",
)


@dataclass(frozen=True, slots=True)
class CentreKnotOption:
    title: str
    centre_knot: str
    archetype: str
    genre: str
    dramatic_engine: str


@dataclass(frozen=True, slots=True)
class CharacterOption:
    name: str
    role: str
    external_objective: str
    internal_need: str
    contradiction: str
    behavior_signature: str
    voice: str
    arc: str


def suggest_centre_knots(seed: str = "", genre: str = "Comedy") -> tuple[CentreKnotOption, ...]:
    subject = seed.strip() or "an ordinary person guarding a private failure"
    return (
        CentreKnotOption(
            "The Impossible Performance",
            f"When {subject} is mistaken for an expert, they must sustain the lie long enough to save the one person who knows the truth.",
            "Comedy",
            genre or "Comedy",
            "Every apparent solution deepens the public deception.",
        ),
        CentreKnotOption(
            "The Reluctant Quest",
            f"When {subject} receives an unwanted last request, they cross a hostile world to deliver it before a rival can erase its meaning.",
            "The Quest",
            genre or "Adventure",
            "Progress forces increasingly costly moral choices.",
        ),
        CentreKnotOption(
            "The Second Chance",
            f"After {subject} loses what defined them, an unlikely dependent forces them to rebuild it without repeating the original betrayal.",
            "Rebirth",
            genre or "Drama",
            "External repair exposes the internal flaw that caused the loss.",
        ),
    )


def suggest_characters(state: NarrativeState) -> tuple[CharacterOption, ...]:
    genre = state.genre or "drama"
    return (
        CharacterOption(
            "The Builder",
            "Protagonist",
            "Solve the external problem at the centre of the plot.",
            "Replace control with earned trust.",
            "Competent in public, terrified of being known privately.",
            "Plans three steps ahead, then improvises when people disrupt the plan.",
            f"Precise language that fractures under {genre.lower()} pressure.",
            "Moves from controlling the outcome to taking responsibility for a truthful choice.",
        ),
        CharacterOption(
            "The Counterforce",
            "Antagonist",
            "Secure the same scarce outcome for an opposing reason.",
            "Recognize that winning cannot repair the originating wound.",
            "Appears ruthless but protects one inviolable tenderness.",
            "Turns every private weakness into a public deadline.",
            "Economical, calm and unsettlingly specific.",
            "Escalates from obstacle to mirror, revealing the protagonist's possible failure-state.",
        ),
        CharacterOption(
            "The Truth Teller",
            "Supporting",
            "Force the protagonist to confront what the plot lets them avoid.",
            "Risk belonging in order to speak honestly.",
            "Uses humor when most emotionally exposed.",
            "Notices behavior rather than accepting explanations.",
            "Concrete observations, misdirection, then one clean truth.",
            "Moves from commentator to consequential participant.",
        ),
        CharacterOption(
            "The Living Stake",
            "Supporting",
            "Obtain safety without becoming a passive prize.",
            "Claim agency inside a conflict designed by others.",
            "Vulnerable in circumstance, decisive in action.",
            "Changes the plan through one unexpected choice.",
            "Few words; each changes the emotional balance.",
            "Transforms from protected object into the person who determines the ending.",
        ),
    )


def draft_full_plot(state: NarrativeState) -> str:
    protagonist = next(
        (c.name for c in state.characters if c.role == "Protagonist"), "the protagonist"
    )
    counterforce = next(
        (c.name for c in state.characters if c.role == "Antagonist"), "the counterforce"
    )
    knot = state.centre_knot or state.premise or "A protagonist faces a consequential disruption."
    objective = state.protagonist_objective or "restore control before the opportunity closes"
    stakes = state.stakes or "failure costs both the visible goal and an essential relationship"
    ending = (
        state.ending or "the final choice resolves the external problem and exposes the inner truth"
    )
    return "\n\n".join(
        (
            f"SETUP — {knot} {protagonist} begins with a practiced way of surviving the world, but that method already conceals the flaw the story will test.",
            f"DISRUPTION — An irreversible event makes the need to {objective} urgent. Refusal produces an immediate loss, so {protagonist} enters the conflict under the wrong emotional assumption.",
            f"PROGRESSIVE COMPLICATIONS — Early tactics appear to work. {counterforce} converts each success into a harder choice, and allies develop objectives that no longer fit the plan. The dramatic promise of {state.plot_archetype or 'the chosen plot'} becomes visible through escalating action.",
            f"MIDPOINT REVERSAL — New information changes the meaning of the goal. {protagonist} gains agency but loses innocence: victory now carries the cost that {stakes}.",
            f"CRISIS — The old strategy fails publicly and damages the relationship that matters most. With no clean option left, {protagonist} must choose between preserving identity and acting from the emerging internal need.",
            f"CLIMAX AND RESOLUTION — {ending}. The resolution pays off the centre knot through behavior, not explanation, and leaves a final image that demonstrates what changed.",
        )
    )


def recommend_structure(state: NarrativeState) -> tuple[str, str]:
    text = " ".join((state.plot_archetype, state.genre, state.tone, state.centre_knot)).lower()
    if any(
        word in text
        for word in ("memory", "mystery", "fragment", "time", "nonlinear", "non-linear")
    ):
        return (
            "Non-linear",
            "The story's meaning depends on when information is revealed, so chronology can become a dramatic tool.",
        )
    if state.plot_archetype == "Tragedy":
        return (
            "Freytag's Pyramid",
            "A visible rise, crisis and irreversible fall best expose the tragic causal chain.",
        )
    if state.genre.lower() in {"action", "thriller", "adventure"}:
        return (
            "Save the Cat",
            "A denser sequence of external turns helps a high-momentum genre maintain escalation.",
        )
    if state.plot_archetype in {"The Quest", "Voyage and Return"}:
        return (
            "Seven Point Story",
            "Seven major turns give the journey causal destinations without prescribing every scene.",
        )
    return (
        "Three Act",
        "Three Act is the clearest default: setup and commitment, escalating confrontation, then crisis and resolution.",
    )


_BEATS: dict[str, tuple[tuple[str, str, str], ...]] = {
    "Three Act": (
        ("Opening State", "Act I", "Establish the protagonist's world, method and incompleteness."),
        ("Inciting Disruption", "Act I", "Make the centre knot unavoidable."),
        ("Act I Commitment", "Act I", "The protagonist chooses the dramatic journey."),
        ("First Escalation", "Act II", "Early action works but enlarges the conflict."),
        ("Midpoint Reversal", "Act II", "Change the meaning, agency or cost of the goal."),
        ("Crisis", "Act II", "Destroy the old strategy and force the defining choice."),
        ("Climax", "Act III", "Resolve external and internal conflict through action."),
        ("New Equilibrium", "Act III", "Show the consequence and transformation."),
    ),
    "Freytag's Pyramid": (
        ("Exposition", "Movement I", "Establish forces already under pressure."),
        ("Inciting Action", "Movement I", "Begin the irreversible causal chain."),
        ("Rising Action", "Movement II", "Escalate gains, costs and opposition."),
        ("Climax", "Movement III", "Reach the decisive peak or reversal."),
        ("Falling Action", "Movement IV", "Let consequences close remaining options."),
        ("Denouement", "Movement V", "Reveal the final moral and emotional state."),
    ),
    "Seven Point Story": (
        ("Opening Hook", "Beginning", "Contrast the protagonist with the ending state."),
        ("Plot Turn One", "Beginning", "Introduce conflict and cross the threshold."),
        ("Pinch One", "Middle", "Apply the counterforce directly."),
        ("Midpoint", "Middle", "Move the protagonist from reaction to action."),
        ("Pinch Two", "Middle", "Make the threat personal and overwhelming."),
        ("Plot Turn Two", "End", "Supply the final truth, tool or choice."),
        ("Resolution", "End", "Complete external action and internal transformation."),
    ),
    "Save the Cat": (
        ("Opening Image", "Act I", "Express the story before-state visually."),
        ("Theme and Setup", "Act I", "Plant the argument, flaw, world and relationships."),
        ("Catalyst", "Act I", "Disrupt the existing order."),
        ("Break into Two", "Act I", "Choose the unfamiliar dramatic world."),
        ("Promise and Progress", "Act II", "Deliver the genre promise through attempts."),
        ("Midpoint", "Act II", "Create a false victory or defeat and raise the stakes."),
        ("Pressure and Collapse", "Act II", "Close options and expose the internal flaw."),
        ("Break into Three", "Act III", "Combine plot knowledge with thematic growth."),
        ("Finale", "Act III", "Execute the transformed solution."),
        ("Final Image", "Act III", "Show the changed equilibrium."),
    ),
    "Non-linear": (
        ("Present-tense Question", "Frame", "Open with the mystery or emotional consequence."),
        ("First Dislocated Cause", "Past", "Reveal a cause that changes the opening."),
        ("Present Escalation", "Frame", "Make the unanswered past operationally urgent."),
        ("Contradictory Memory", "Past", "Challenge the audience's causal model."),
        ("Convergence", "Threshold", "Join timelines at the defining choice."),
        ("Recontextualized Climax", "Resolution", "Resolve action and reinterpret earlier scenes."),
        ("Final Chronological Truth", "Coda", "Leave one coherent emotional meaning."),
    ),
}


def structure_beats(structure_type: str) -> tuple[tuple[str, str, str], ...]:
    return _BEATS.get(structure_type, _BEATS["Three Act"])


def phase_completion(state: NarrativeState) -> tuple[bool, ...]:
    return (
        all((state.centre_knot, state.plot_archetype, state.genre, state.central_conflict)),
        len(state.characters) >= 2 and any(c.role == "Protagonist" for c in state.characters),
        bool(state.full_plot and state.stakes and state.ending),
        bool(state.structure_type and state.beats and all(beat.event for beat in state.beats)),
        bool(state.scenes)
        and all(scene.objective and scene.conflict and scene.outcome for scene in state.scenes),
        5 in state.locked_phases,
    )

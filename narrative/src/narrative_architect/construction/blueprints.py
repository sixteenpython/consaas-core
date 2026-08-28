# ruff: noqa: E501
"""Skill-backed deterministic blueprints used with or without a local model."""

from __future__ import annotations

import re
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


@dataclass(frozen=True, slots=True)
class SceneBlueprint:
    """A deterministic, story-grounded scene proposal for author review."""

    heading: str
    summary: str
    location: str
    time_of_day: str
    structural_beat_id: str
    viewpoint_character_id: str
    entry_state: str
    objective: str
    conflict: str
    escalation: str
    turning_point: str
    outcome: str
    emotional_change: str
    character_behavior: str
    dialogue_context: str
    dialogue_text: str
    dialogue_subtext: str
    blocking: str
    setup_payoff: str
    character_ids: tuple[str, ...]


_LOCATION_RULES = (
    (("accountant", "ledger", "budget", "invoice"), "palace accounts office"),
    (("chef", "cook", "feast", "banquet", "oven"), "royal kitchen"),
    (("wedding", "bride", "groom"), "wedding banquet hall"),
    (("lighthouse", "beacon", "lantern"), "lighthouse lantern room"),
    (("signal", "radio", "transmission", "frequency"), "radio room"),
    (("ferry", "harbor", "harbour", "dock"), "storm harbor"),
    (("court", "judge", "trial"), "courtroom"),
    (("hospital", "doctor", "patient"), "hospital ward"),
    (("school", "teacher", "student", "class"), "classroom"),
    (("train", "station", "platform"), "railway platform"),
    (("hotel", "guest", "lobby"), "hotel lobby"),
    (("restaurant", "waiter", "diner"), "restaurant dining room"),
    (("stage", "actor", "audience", "performance"), "backstage corridor"),
    (("ship", "captain", "deck"), "ship's bridge"),
    (("laboratory", "laboratory", "experiment", "scientist"), "laboratory"),
    (("office", "clerk", "manager"), "administration office"),
    (("home", "house", "family"), "family home"),
)

_PROP_RULES = (
    (
        ("accountant", "budget", "invoice", "ledger"),
        ("ledger", "invoice", "ink-stained calculation"),
    ),
    (("chef", "cook", "feast", "kitchen"), ("chef's coat", "serving tray", "unlit oven")),
    (("lighthouse", "beacon"), ("beacon switch", "storm glass", "generator gauge")),
    (("signal", "radio", "transmission"), ("radio dial", "written coordinates", "power cable")),
    (("wedding", "banquet"), ("seating chart", "wedding menu", "covered platter")),
    (("court", "trial"), ("case file", "witness chair", "sealed exhibit")),
    (("school", "class"), ("attendance register", "chalkboard", "locked desk")),
)


def _clean_sentence(value: str) -> str:
    text = re.sub(r"^[A-Z][A-Z /&-]{2,24}\s*[—:-]\s*", "", value.strip())
    text = re.sub(r"\s*\([^)]{10,}\)\s*$", "", text).strip()
    if not text:
        return "The approved story event becomes unavoidable"
    return text.rstrip(". ") + "."


def _story_corpus(state: NarrativeState, event: str = "") -> str:
    return " ".join(
        (
            event,
            state.centre_knot,
            state.central_conflict,
            state.full_plot,
            state.stakes,
            state.ending,
        )
    ).lower()


def _location_for(state: NarrativeState, event: str, ordinal: int) -> str:
    event_text = event.lower()
    corpus = _story_corpus(state, event)
    ranked: list[tuple[int, int, str]] = []
    for index, (keywords, location) in enumerate(_LOCATION_RULES):
        event_hits = sum(keyword in event_text for keyword in keywords)
        corpus_hits = sum(keyword in corpus for keyword in keywords)
        ranked.append((event_hits * 10 + corpus_hits, -index, location))
    best_score, _index, best_location = max(ranked)
    if best_score:
        if (
            ordinal > 1
            and best_location == "palace accounts office"
            and any(word in corpus for word in ("chef", "cook", "feast", "kitchen"))
        ):
            return "royal kitchen"
        return best_location
    title = re.sub(r"[^A-Za-z0-9 ]+", " ", state.title).strip()
    return f"{title or 'story'} workroom"


def _props_for(state: NarrativeState, event: str) -> tuple[str, str, str]:
    event_text = event.lower()
    corpus = _story_corpus(state, event)
    ranked: list[tuple[int, tuple[str, str, str]]] = []
    for keywords, props in _PROP_RULES:
        event_hits = sum(keyword in event_text for keyword in keywords)
        corpus_hits = sum(keyword in corpus for keyword in keywords)
        ranked.append((event_hits * 10 + corpus_hits, props))
    score, props = max(ranked, key=lambda item: item[0])
    if score:
        return props
    return ("doorway", "working table", "object named in the approved event")


def _time_for(event: str, ordinal: int, total: int) -> str:
    lowered = event.lower()
    if "dawn" in lowered:
        return "DAWN"
    if any(word in lowered for word in ("night", "midnight", "dark")):
        return "NIGHT"
    if any(word in lowered for word in ("dusk", "sunset", "evening")):
        return "DUSK"
    if ordinal == total and "morning" in lowered:
        return "MORNING"
    return "DAY"


def _as_action(value: str, fallback: str) -> str:
    text = value.strip().rstrip(".") or fallback
    return text[0].lower() + text[1:] if text else fallback


def build_scene_blueprints(state: NarrativeState) -> tuple[SceneBlueprint, ...]:
    """Translate the approved structure into specific, causally linked scene proposals.

    The method intentionally uses only canonical NKA material. It does not pretend that
    deterministic drafting replaces an author's craft pass or local-model elaboration.
    """

    if not state.beats:
        return ()
    protagonist = next(
        (character for character in state.characters if character.role == "Protagonist"),
        state.characters[0] if state.characters else None,
    )
    counterforce = next(
        (character for character in state.characters if character.role == "Antagonist"),
        next((character for character in state.characters if character is not protagonist), None),
    )
    protagonist_name = protagonist.name if protagonist else "The protagonist"
    counterforce_name = counterforce.name if counterforce else "The opposing force"
    protagonist_goal = _as_action(
        protagonist.external_objective if protagonist else state.protagonist_objective,
        "complete the approved objective",
    )
    counterforce_goal = _as_action(
        counterforce.external_objective if counterforce else "",
        "prevent the protagonist from controlling the outcome",
    )
    behavior = _as_action(
        protagonist.behavior_signature if protagonist else "",
        "uses the familiar tactic that has protected them until now",
    )
    opposition_behavior = _as_action(
        counterforce.behavior_signature if counterforce else "",
        "turns the protagonist's private weakness into a public deadline",
    )
    arc = protagonist.arc if protagonist and protagonist.arc else state.theme
    fear = protagonist.fear if protagonist and protagonist.fear else state.stakes
    contradiction = protagonist.contradiction if protagonist and protagonist.contradiction else arc
    internal_need = (
        protagonist.internal_need if protagonist and protagonist.internal_need else state.theme
    )
    internal_need_action = _as_action(internal_need, "face the emerging need")
    fear_clause = _as_action(fear, "the declared loss becomes real")
    participant_ids = tuple(
        character.character_id for character in (protagonist, counterforce) if character
    )
    blueprints: list[SceneBlueprint] = []
    total = len(state.beats)
    for index, beat in enumerate(state.beats):
        event = _clean_sentence(beat.event)
        previous_event = (
            _clean_sentence(state.beats[index - 1].event)
            if index
            else _clean_sentence(state.centre_knot)
        )
        next_beat = state.beats[index + 1] if index + 1 < total else None
        next_event = (
            _clean_sentence(next_beat.event) if next_beat else _clean_sentence(state.ending)
        )
        location = _location_for(state, event, beat.ordinal)
        time_of_day = _time_for(event, beat.ordinal, total)
        prop_one, prop_two, prop_three = _props_for(state, event)
        event_without_period = event.rstrip(".")
        next_without_period = next_event.rstrip(".")
        summary = (
            f"{event} Inside the {location}, {protagonist_name} {behavior}. "
            f"{counterforce_name} {opposition_behavior}. The {prop_one} becomes the point of struggle: "
            f"{protagonist_name} reaches for it to {protagonist_goal}, {counterforce_name} blocks access, "
            f"and the resulting action sets up the next event—{next_without_period}."
        )
        entry_state = (
            f"The scene inherits a concrete consequence from the previous movement: "
            f"{previous_event} {protagonist_name} enters the {location} still trying to {protagonist_goal}."
        )
        objective = (
            f"{protagonist_name} wants to {protagonist_goal}, but must first resolve the immediate "
            f"problem inside {beat.label.lower()}: {event_without_period}."
        )
        conflict = (
            f"{counterforce_name} acts to {counterforce_goal}, directly obstructing {protagonist_name}; "
            f"the collision makes the central conflict playable: {state.central_conflict.rstrip('.')}."
        )
        escalation = (
            f"{protagonist_name}'s usual tactic—{behavior}—backfires around the {prop_one}; "
            f"the resulting exposure brings the declared stakes into the room: {state.stakes.rstrip('.')}."
        )
        turning_point = (
            f"When {next_without_period.lower()}, {protagonist_name} chooses to {protagonist_goal} "
            f"rather than let {counterforce_name} {counterforce_goal}."
        )
        outcome = (
            f"The choice gives {protagonist_name} temporary control of the {prop_one} and commits "
            f"both characters to the next event: {next_without_period}."
        )
        emotional_change = (
            f"The choice cracks {protagonist_name}'s contradiction—"
            f"{contradiction.rstrip('.')}—and moves the character toward the need to "
            f"{internal_need_action}, while {fear_clause} remains the cost."
            if arc
            else f"{protagonist_name} leaves less able to rely on the strategy used on entry."
        )
        character_behavior = (
            f"Under pressure, {protagonist_name} first {behavior}; after the turn, the choice to "
            f"{protagonist_goal} reveals movement toward the need to {internal_need_action}."
        )
        dialogue_context = (
            f"{protagonist_name} needs to {protagonist_goal}; {counterforce_name} needs to "
            f"{counterforce_goal}. Neither can concede while {state.stakes.rstrip('.')} remains possible."
        )
        dialogue_text = f"I can still {protagonist_goal}. Help me now, or tell everyone why you chose to stop me."
        dialogue_subtext = (
            f"{protagonist_name} speaks as if the argument is about the task, while concealing "
            f"the deeper need to {internal_need_action} and the fear that {fear_clause}."
        )
        blocking = (
            f"The {prop_one}, {prop_two} and {prop_three} divide the {location} into competing zones of control. "
            f"{counterforce_name} blocks access to the {prop_one}; the turn becomes visible when "
            f"{protagonist_name} crosses that barrier and takes possession of it."
        )
        setup_payoff = (
            f"The unresolved struggle over the {prop_one} becomes the physical setup for "
            f"{next_beat.label if next_beat else 'the final image'}: {next_without_period}."
        )
        blueprints.append(
            SceneBlueprint(
                heading=f"INT. {location.upper()} - {time_of_day}",
                summary=summary,
                location=location,
                time_of_day=time_of_day,
                structural_beat_id=beat.beat_id,
                viewpoint_character_id=protagonist.character_id if protagonist else "",
                entry_state=entry_state,
                objective=objective,
                conflict=conflict,
                escalation=escalation,
                turning_point=turning_point,
                outcome=outcome,
                emotional_change=emotional_change,
                character_behavior=character_behavior,
                dialogue_context=dialogue_context,
                dialogue_text=dialogue_text,
                dialogue_subtext=dialogue_subtext,
                blocking=blocking,
                setup_payoff=setup_payoff,
                character_ids=participant_ids,
            )
        )
    return tuple(blueprints)


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

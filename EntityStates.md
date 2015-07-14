| **state** | **destination** | **next state** | **facing** | **animation** |
|:----------|:----------------|:---------------|:-----------|:--------------|
| _stand_ (default state, also after hit, defend, finishAttack or finishHealing, or being healed) | home            | stand          | forward    | healthy or injured |
| _lie_ (when incapacitated - at the beginning of enemy's finishAttack) | current position | lie            | either     | incapacitated |
| _hit_ (at the beginning of enemy's finishAttack) | home            | stand          | forward    | pain          |
| _defend_ (at the beginning of enemy's finishAttack) | home            | stand or fear  | either     | block         |
| _fear_ (leaving - when the character chooses escape, after defend or being healed while fleeing) | home            | fear           | backward   | healthy or injured |
| _run_ (gone - when an entity begins a turn while trying to escape) | off screen      | run            | backward   | healthy or injured |
| _wait_ (when the entity begins a turn but is not incapacitated, leaving or gone) | center          | wait           | forward    | healthy or injured |
| _headToAttack_ (when the character chooses to attack an enemy on his turn) | partway to target | beginAttack    | forward    | healthy or injured |
| _beginAttack_ (after headToAttack) | target          | finishAttack   | forward    | attack        |
| _finishAttack_ (after beginAttack) | partway home    | stand          | forward    | attack        |
| _healSelf_ (when the character chooses to target himself on his turn) | one step backward | stand          | forward    | injured       |
| _headToHeal_ (when the character chooses an ally target on his turn) | partway to target | beginHealing   | backward   | healthy or injured |
| _beginHealing_ (after headToHeal) | target          | finishHealing  | backward   | heal          |
| _finishHealing_ (after beginHealing) | partway home    | stand          | backward   | heal          |